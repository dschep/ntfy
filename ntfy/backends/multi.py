from importlib import import_module
try:
    from ..terminal import is_focused
except ImportError:
    def is_focused():
        return True
from ..screensaver import is_locked


def notify(title,
           message,
           locked=None,
           focused=None,
           unfocused=None,
           retcode=None):
    for condition, options in ((is_locked, locked),
                               (is_focused, focused),
                               (lambda: not is_focused(), unfocused)):
        for backend_name, backend_options in options.items():
            if not condition():
                continue
            backend = import_module('ntfy.backends.{}'.format(
                backend_options.get('backend', backend_name)))
            backend_options.pop('backend', None)
            backend.notify(title, message, retcode=retcode, **backend_options)
