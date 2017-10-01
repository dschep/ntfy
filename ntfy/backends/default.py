from importlib import import_module
from sys import platform


class DefaultNotifierError(Exception):
    def __init__(self, exception, module):
        self.exception = exception
        self.module = module


def notify(title, message, **kwargs):
    """
    This backend automatically selects the correct desktop notification backend
    for your operating system.
    """
    for os in ['linux', 'win32', 'darwin']:
        if platform.startswith(os):
            module = import_module('ntfy.backends.{}'.format(os))
            try:
                module.notify(title=title, message=message, **kwargs)
            except Exception as e:
                raise DefaultNotifierError(e, module)
            break
