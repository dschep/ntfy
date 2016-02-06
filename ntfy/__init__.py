import pkg_resources
import logging
from importlib import import_module

from .config import load_config

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


def notify(message, title, config=None, **kwargs):
    if config is None:
        config = load_config()

    ret = 0

    for backend in config['backends']:
        module = import_module('ntfy.backends.{}'.format(backend))

        backend_config = config.get(backend, {})
        backend_config.update(kwargs)

        try:
            module.notify(message=message, title=title, **backend_config)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logging.getLogger(__name__).error(
                'Failed to send notification using {}'.format(backend),
                exc_info=True)
            ret = 1

    return ret
