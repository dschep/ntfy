import argparse
import errno
import json
import logging
import logging.config
from os.path import expanduser
from getpass import getuser
from importlib import import_module
from socket import gethostname
from subprocess import call
from sys import exit
from time import time

from emoji import emojize

from . import __version__


def truthyish(value):
    """
    same as standard python truthyness except that strings are different.
    True, t, yes, y and 1 (case insensitive) are considered truthy.
    """
    if isinstance(value, str):
        return value.lower() in ('true', 't', 'yes', 'y', '1')
    else:
        return bool(value)


def load_config(args):
    logger = logging.getLogger(__name__)

    #import pdb;pdb.set_trace()
    try:
        config = json.load(open(expanduser(args.config)))
    except IOError as e:
        if e.errno == errno.ENOENT and args.config == '~/.ntfy.json':
            logger.warning('{.config} not found'.format(args))
            config = {'backends': ['default']}
        else:
            logger.error('Failed to open {.config}'.format(args),
                         exc_info=True)
            exit(1)
    except ValueError as e:
        logger.error('Failed to load {.config}', exc_info=True)
        import pdb;pdb.set_trace()
        exit(1)

    if 'backend' in config:
        if 'backends' in config:
            logger.warning("Both 'backend' and 'backends' in config, "
                           "ignoring 'backend'.")
        else:
            config['backends'] = [config['backend']]

    if args.backend:
        config['backends'] = args.backend

    return config


def run_cmd(args):
    start_time = time()
    retcode = call(args.command)
    return '"{}" {} in {:d}:{:02d} minutes'.format(
        ' '.join(args.command),
        'succeeded' if retcode == 0 else 'failed',
        *map(int, divmod(time() - start_time, 60))
    )


def send_notification(message, args, config):
    ret = 0

    for backend in config['backends']:
        module = import_module('ntfy.backends.{}'.format(backend))

        backend_config = config.get(backend, {})
        backend_config.update(args.option)
        use_emoji = not truthyish(backend_config.get('disable_emoji', ''))

        try:
            module.notify(title=args.title,
                          message=(emojize(message, use_aliases=True)
                                   if use_emoji else message),
                          **backend_config)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logging.getLogger(__name__).error(
                'Failed to send notification using {}'.format(backend),
                exc_info=True)
            ret = 1

    return ret

parser = argparse.ArgumentParser(
    description='Send push notification when command finishes')

parser.add_argument('-c', '--config',
                    default='~/.ntfy.json',
                    help='config file to use (default: ~/.ntfy.json)')
parser.add_argument('-b', '--backend', action='append',
                    help='override backend specified in config')
parser.add_argument('-o', '--option', nargs=2, action='append',
                    metavar=('key', 'value'), default=[],
                    help='backend specific options')
parser.add_argument('-l', '--log-level', action='store',
                    default='WARNING', choices=[
                        'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                    help=('Specify the how verbose CLI output is '
                          '(default: WARNING)'))
parser.add_argument('-v', '--version', action='version',
                    version=__version__)

default_title = '{}@{}'.format(getuser(), gethostname())

parser.add_argument('-t', '--title', default=default_title,
                    help='a title for the notification (default: {})'
                    .format(default_title))
parser.add_argument('-d', '--device', help='device to notify')

subparsers = parser.add_subparsers()

send_parser = subparsers.add_parser('send', help='send a notification')
send_parser.add_argument('message',
                         help='notification message')
send_parser.set_defaults(func=lambda args: args.message)

done_parser = subparsers.add_parser(
    'done', help='run a command and send a notification when done')
done_parser.add_argument('command',
                         nargs=argparse.REMAINDER,
                         help='command to run')
done_parser.set_defaults(func=run_cmd)


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

    config = load_config(args)

    if hasattr(args, 'func'):
        return send_notification(args.func(args), args, config)
    else:
        parser.print_help()

if __name__ == '__main__':
    exit(main())
