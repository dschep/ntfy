from sys import platform
from importlib import import_module


def notify(subject, config, message=None, device=None):
    for os in ['linux', 'darwin']:
        if platform.startswith(os):
            module = import_module('ntfy.backends.{}'.format(os))
            module.notify(subject, config, message, device)
            break
