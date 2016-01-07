import argparse
import json
from os.path import expanduser
from getpass import getuser
from importlib import import_module
from socket import gethostname
from subprocess import call
from sys import stderr, exit
from time import time

from requests import HTTPError


def load_config(args):
    try:
        config = json.load(open(expanduser(args.config)))
    except IOError:
        stderr.write(
            "Warning: Couldn't open config file '{.config}'.\n".format(args))
        config = {'backends': ['default']}

    if 'backend' in config:
        if 'backends' in config:
            stderr.write("Warning: both 'backend' and 'backends' in config, "
                         "ignoring 'backend'.\n")
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

        try:
            module.notify(title=args.title, message=message,
                          config=config.get(backend, {}),
                          **dict(args.option))
        except HTTPError as e:
            stderr.write(
                'Error: status={resp.status_code} body={resp.content}\n'.format(
                    resp=e.response))
            ret = 1

    return ret


def main():
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

    args = parser.parse_args()
    config = load_config(args)

    if hasattr(args, 'func'):
        return send_notification(args.func(args), args, config)
    else:
        parser.print_help()

if __name__ == '__main__':
    exit(main())
