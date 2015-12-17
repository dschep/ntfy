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

    parser.add_argument('-t', '--title', metavar='TITLE',
                        default=default_title,
                        help='a title for the notification (default: {})'
                        .format(default_title))
    parser.add_argument('-d', '--device', help='device to notify')
    parser.add_argument('-c', '--config', metavar='CONFIG_FILE',
                        default='~/.ntfy.json',
                        help='config file to use (default: ~/.ntfy.json)')
    parser.add_argument('-b', '--backend', metavar='BACKEND',
                        help='override backend specified in config')


def load_config(args):
    config = json.load(open(expanduser(args.config)))

    if args.backend:
        config['backend'] = args.backend

    return config


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


def notify():
    parser = argparse.ArgumentParser(
        description='Send push notification')

    parser.add_argument('message', metavar='MESSAGE', nargs=argparse.REMAINDER,
                        help='notification message')

    add_common_args(parser)
    args = parser.parse_args()
    config = load_config(args)

    message = ' '.join(args.message)

    return send_notification(message, args, config)

def notify_done():
    parser = argparse.ArgumentParser(
        description='Send push notification when command finishes')

    parser.add_argument('command', metavar='COMMAND', nargs=argparse.REMAINDER,
                        help='command to run')

    add_common_args(parser)
    args = parser.parse_args()
    config = load_config(args)

    start_time = time()
    retcode = call(args.command)
    message = '"{}" {} in {:.1f} minutes'.format(
        ' '.join(args.command),
        'succeeded' if retcode == 0 else 'failed',
        (time() - start_time) / 60,
    )

    return send_notification(message, args, config)

if __name__ == '__main__':
    exit(notify())
