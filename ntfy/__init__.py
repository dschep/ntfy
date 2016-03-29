import pkg_resources
import logging
from importlib import import_module

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

try:
    from dbus.exceptions import DBusException
except ImportError:

    class DBusException(Exception):
        pass

from . import vendor


def notify(message, title, config=None, **kwargs):
    from .config import load_config

    if config is None:
        config = load_config()

    ret = 0

    for backend in config.get('backends', ['default']):
        backend_config = config.get(backend, {})
        backend_config.update(kwargs)
        if 'backend' in backend_config:
            backend = backend_config['backend']
        try:
            module = import_module('ntfy.backends.{}'.format(backend))
        except ImportError:
            ret = 1
            logging.getLogger(__name__).error(
                'failed to load backend {}'.format(backend),
                exc_info=True)
            continue

        try:
            module.notify(message=message, title=title, **backend_config)
        except (SystemExit, KeyboardInterrupt):
            raise
        except DBusException:
            logging.getLogger(__name__).warning(
                'Failed to send notification using {}'.format(backend))
        except Exception:
            logging.getLogger(__name__).error(
                'Failed to send notification using {}'.format(backend),
                exc_info=True)
            ret = 1

    return ret
