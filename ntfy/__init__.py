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

    ret = 1
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
            logging.getLogger(__name__).error(
                'Invalid backend {}'.format(backend))

        if not notifier:
            logging.getLogger(__name__).error(
                'failed to load backend {}'.format(backend))
        else:
            try:
                notifier.notify(message=message, title=title, retcode=retcode,
                                **backend_config)
                ret = 0
            except (SystemExit, KeyboardInterrupt):
                raise
            except Exception:
                import sys
                if sys.version_info.major == 3 and sys.version_info.minor not in [0, 1, 2, 3, 4]:
                    exc_info = False
                else:
                    exc_info = True
                logging.getLogger(__name__).error(
                    'Failed to send notification using {}'.format(backend),
                    exc_info=exc_info)

    return ret
