import logging
from importlib import import_module

__version__ = '2.0.4'


notifiers = {'default': None, 'darwin': None, 'linux': None,
             'darwin': None, 'pushbullet': None, 'pushover': None,
             'telegram': None, 'win32': None, 'xmpp': None}


for k, v in notifiers.items():
    try:
        module = import_module('ntfy.backends.{}'.format(k))
        notifiers[k] = module
    except (ImportError, OSError):
        continue


def notify(message, title, config=None, **kwargs):
    from .config import load_config

    if config is None:
        config = load_config()

    ret = 0
    retcode = kwargs.pop('retcode', None)

    for backend in config.get('backends', ['default']):
        backend_config = config.get(backend, {})
        backend_config.update(kwargs)
        if 'backend' in backend_config:
            backend = backend_config['backend']

        notifier = None
        try:
            notifier = notifiers[backend]
        except KeyError:
            ret = 1
            logging.getLogger(__name__).error(
                'Invalid backend {}'.format(backend),
                exc_info=True)

        if not notifier:
            ret = 1
            logging.getLogger(__name__).error(
                'failed to load backend {}'.format(backend),
                exc_info=True)

        try:
            notifier.notify(message=message, title=title, retcode=retcode, **backend_config)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logging.getLogger(__name__).error(
                'Failed to send notification using {}'.format(backend),
                exc_info=True)
            ret = 1

    return ret
