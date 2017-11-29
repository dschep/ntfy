import argparse
import logging
import logging.config
import sys
from os import environ, path
from subprocess import PIPE, STDOUT, Popen
from time import time

from . import __version__, default_title, notify
from .config import (DEFAULT_CONFIG, OLD_DEFAULT_CONFIG, SITE_DEFAULT_CONFIG,
                     load_config)
from .data import scripts

try:
    from shlex import quote as sh_quote
except ImportError:
    from pipes import quote as sh_quote

try:
    from emoji import emojize
except ImportError:
    emojize = None

try:
    import psutil
except ImportError:
    psutil = None

try:
    from .terminal import is_focused
except ImportError:

    def is_focused():
        return True


def run_cmd(args):
    if getattr(args, 'pid', False):
        return watch_pid(args)
    if not args.command:
        if args.formatter:
            args.command, retcode, duration = args.formatter
            args.command, retcode, duration = ([args.command], int(retcode),
                                               int(duration))
            args.option.setdefault('linux', {}).setdefault('transient', 'true')
            stdout, stderr = None, None
        else:
            sys.stderr.write('usage: ntfy done [-h|-L N] command\n'
                             'ntfy done: error: the following arguments '
                             'are required: command\n')
            sys.exit(1)
    else:
        if args.stdout and args.stderr:
            out = PIPE
            err = STDOUT
        else:
            out = PIPE if args.stdout else None
            err = PIPE if args.stderr else None
        start_time = time()
        process = Popen(args.command, stdout=out, stderr=err)
        stdout, stderr = process.communicate()
        process.wait()
        duration = time() - start_time
        retcode = process.returncode
    if args.longer_than is not None and duration <= args.longer_than:
        return None, None
    if args.unfocused_only and is_focused():
        return None, None
    message = _result_message(args.command if not args.hide_command else None,
                              retcode, stdout, stderr, duration,
                              emojize is not None and not args.no_emoji)
    return message, retcode


def _result_message(command, return_code, stdout, stderr, duration, emoji):
    if emoji:
        prefix = ':white_check_mark: ' if return_code == 0 else ':x: '
    else:
        prefix = ''
    if return_code == 0:
        result = 'succeeded'
    else:
        result = 'failed (code {:d})'.format(return_code)
    if command is None:
        command = 'Your command'
    else:
        command = '"{command}"'.format(command=' '.join(command))
    if stdout is not None or stderr is not None:
        all_output = ':\n{}{}'.format(stdout
                                      if stdout is not None else '', stderr
                                      if stderr is not None else '')
    else:
        all_output = ''
    template = '{prefix}{command} {result} in {:d}:{:02d} minutes{output}'
    return template.format(
        prefix=prefix,
        command=command,
        result=result,
        output=all_output,
        *map(int, divmod(duration, 60)))


def watch_pid(args):
    if psutil is None:  # pragma: no cover
        logging.error(
            "This command requires psutil module. Pleases install psutil.")
        sys.exit(1)
    try:
        p = psutil.Process(args.pid)
        cmd = p.cmdline()
        start_time = p.create_time()
    except psutil.NoSuchProcess:
        logging.error("PID {} not found".format(args.pid))
        sys.exit(1)
    ret = None
    try:
        ret = p.wait()
    except psutil.NoSuchProcess:  # pragma: no cover
        pass  # this happens when the PID disapears
    duration = time() - start_time
    return 'PID[{}]: "{}" finished in {:d}:{:02d} minutes'.format(
        p.pid, ' '.join(cmd), *map(int, divmod(duration, 60))), ret


def auto_done(args):
    if args.longer_than:
        print('export AUTO_NTFY_DONE_LONGER_THAN=-L{}'.format(
            args.longer_than))
    if args.unfocused_only:
        print('export AUTO_NTFY_DONE_UNFOCUSED_ONLY=-b')
    if args.shell == 'bash':
        print('source {}'.format(sh_quote(scripts['bash-preexec.sh'])))
    print('source {}'.format(sh_quote(scripts['auto-ntfy-done.sh'])))
    print("# To use ntfy's shell integration, run "
          "this and add it to your shell's rc file:")
    print('# eval "$(ntfy shell-integration)"')
    return None, None


class BackendOptionAction(argparse.Action):
    backend = None

    def __call__(self, parser, args, values, option_string=None):
        if self.dest == 'backend':
            self.__class__.backend = values
            if args.backend is None:
                args.backend = []
            args.backend.append(values)
        elif self.dest == 'option':
            if args.option is None:
                args.option = {}
            args.option.setdefault(self.__class__.backend,
                                   {})[values[0]] = values[1]
        else:
            raise Exception("'BackendOptionAction only supports dest of "
                            "'backend' and 'option'")


parser = argparse.ArgumentParser(
    description='Send push notification when command finishes')

parser.add_argument(
    '-c',
    '--config',
    help='config file to use (default: {})'.format(DEFAULT_CONFIG))
parser.add_argument(
    '-b',
    '--backend',
    action=BackendOptionAction,
    help='override backend specified in config')
parser.add_argument(
    '-o',
    '--option',
    nargs=2,
    default=None,
    action=BackendOptionAction,
    metavar=('key', 'value'),
    help='backend specific options')
parser.add_argument(
    '-l',
    '--log-level',
    action='store',
    default='WARNING',
    choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
    help=('Specify the how verbose CLI output is '
          '(default: WARNING)'))
parser.add_argument(
    '-v',
    '--verbose',
    dest='log_level',
    action='store_const',
    const='DEBUG',
    help='a shortcut for --log-level=DEBUG')
parser.add_argument(
    '-q',
    '--quiet',
    dest='log_level',
    action='store_const',
    const='CRITICAL',
    help='a shortcut for --log-level=CRITICAL')
parser.add_argument('--version', action='version', version=__version__)
if emojize is not None:
    parser.add_argument(
        '-E', '--no-emoji', action='store_true', help='Disable emoji support')

parser.add_argument(
    '-t',
    '--title',
    help='a title for the notification (default: {})'.format(default_title))

subparsers = parser.add_subparsers()

send_parser = subparsers.add_parser('send', help='send a notification')
send_parser.add_argument('message', help='notification message')


def default_sender(args):
    return args.message, 0


send_parser.set_defaults(func=default_sender)

done_parser = subparsers.add_parser(
    'done', help='run a command and send a notification when done')
done_parser.add_argument(
    'command', nargs=argparse.REMAINDER, help='command to run')
done_parser.add_argument(
    '-L',
    '--longer-than',
    type=int,
    metavar='N',
    help="Only notify if the command runs longer than N seconds")
done_parser.add_argument(
    '-b',
    '--background-only',
    action='store_true',
    default=False,
    dest='unfocused_only',
    help="Only notify if shell isn't in the foreground")
done_parser.add_argument(
    '--formatter',
    metavar=('command', 'retcode', 'duration'),
    nargs=3,
    help="Format and send cmd, retcode & duration instead of running command. "
    "Used internally by shell-integration")
if psutil is not None:
    done_parser.add_argument(
        '-p',
        '--pid',
        type=int,
        help="Watch a PID instead of running a new command")
done_parser.add_argument(
    '-o',
    '--stdout',
    action='store_true',
    help="Capture and send standard output")
done_parser.add_argument(
    '-e',
    '--stderr',
    action='store_true',
    help="Capture and send standard error")
done_parser.add_argument(
    '-H',
    '--hide-command',
    action='store_true',
    default=False,
    help="Do not display the executed command in any notifications")
done_parser.set_defaults(func=run_cmd)

shell_integration_parser = subparsers.add_parser(
    'shell-integration',
    help='automatically get notifications when long running commands finish')
shell_integration_parser.add_argument(
    '-s',
    '--shell',
    default=path.split(environ.get('SHELL', ''))[1],
    choices=['bash', 'zsh'],
    help='The shell to integrate ntfy with (default: $SHELL)')
shell_integration_parser.add_argument(
    '-L',
    '--longer-than',
    default=10,
    type=int,
    metavar='N',
    help="Only notify if the command runs longer than N seconds")
shell_integration_parser.add_argument(
    '-f',
    '--foreground-too',
    action='store_false',
    default=True,
    dest='unfocused_only',
    help="Also notify if shell is in the foreground")
shell_integration_parser.set_defaults(func=auto_done)


def main(cli_args=None):
    if cli_args is not None:
        args = parser.parse_args(cli_args)
    else:
        args = parser.parse_args()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(levelname)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': args.log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': args.log_level,
                'propagate': True,
            }
        }
    })

    if args.config is not None:
        config = load_config(args.config)
    elif path.exists(path.expanduser(DEFAULT_CONFIG)):
        config = load_config(DEFAULT_CONFIG)
    elif path.exists(OLD_DEFAULT_CONFIG):
        config = load_config(OLD_DEFAULT_CONFIG)
    elif path.exists(path.expanduser(SITE_DEFAULT_CONFIG)):
        config = load_config(SITE_DEFAULT_CONFIG)
    else:  # get default config and print message about missing file
        config = load_config()

    if 'NTFY_BACKENDS' in environ:
        config['backends'] = environ['NTFY_BACKENDS'].split(',')

    if args.backend:
        config['backends'] = args.backend

    if args.option is None:
        args.option = {}
    for backend, backend_options in args.option.items():
        if backend is not None:
            config.setdefault(backend, {}).update(backend_options)

    if getattr(args, 'func', None) == run_cmd and args.longer_than is None and\
            'longer_than' in config:
        args.longer_than = config['longer_than']

    if getattr(args, 'func', None) == run_cmd and 'hide_command' in config:
        args.hide_command = config['hide_commnad']

    if hasattr(args, 'func'):
        message, retcode = args.func(args)
        if message is None:
            return 0
        if emojize is not None and not args.no_emoji:
            message = emojize(message, use_aliases=True)
        return notify(
            message,
            args.title,
            config,
            retcode=retcode,
            **dict(args.option.get(None, [])))
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
