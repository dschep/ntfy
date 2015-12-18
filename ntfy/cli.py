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



def add_common_args(parser):
    default_title = '{}@{}'.format(getuser(), gethostname())

    parser.add_argument('-t', '--title', default=default_title,
                        help='a title for the notification (default: {})'
                        .format(default_title))
    parser.add_argument('-d', '--device', help='device to notify')


def load_config(args):
    config = json.load(open(expanduser(args.config)))

    if args.backend:
        config['backend'] = args.backend

    return config


def run_cmd(args):
    start_time = time()
    retcode = call(args.command)
    return '"{}" {} in {:.1f} minutes'.format(
        ' '.join(args.command),
        'succeeded' if retcode == 0 else 'failed',
        (time() - start_time) / 60,
    )


def send_notification(message, args, config):
    module = import_module('ntfy.backends.{}'.format(config['backend']))

    try:
        module.notify(message=message, subject=args.title,
                    device=args.device, config=config.get(config['backend'], {}),)
    except HTTPError as e:
        stderr.write(
            'Error: status={resp.status_code} body={resp.content}\n'.format(
                resp=e.response))
        return 1
    else:
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Send push notification when command finishes')

    parser.add_argument('-c', '--config',
                        default='~/.ntfy.json',
                        help='config file to use (default: ~/.ntfy.json)')
    parser.add_argument('-b', '--backend',
                        help='override backend specified in config')

    subparsers = parser.add_subparsers()

    send_parser = subparsers.add_parser('send', help='send a notification')
    add_common_args(send_parser)
    send_parser.add_argument('message',
                             help='notification message')
    send_parser.set_defaults(func=lambda args: args.message)

    done_parser = subparsers.add_parser(
        'done', help='run a command and send a notification when done')
    add_common_args(done_parser)
    done_parser.add_argument('command',
                             nargs=argparse.REMAINDER,
                             help='command to run')
    done_parser.set_defaults(func=run_cmd)

    args = parser.parse_args()
    config = load_config(args)

    if hasattr(args, 'func'):
        send_notification(args.func(args), args, config)
    else:
        parser.print_help()

if __name__ == '__main__':
    exit(main())
