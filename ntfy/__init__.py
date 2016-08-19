import logging
from importlib import import_module
from inspect import getargspec
from .backends.default import DefaultNotifierError

__version__ = '2.1.0'


notifiers = {'default': None, 'darwin': None, 'linux': None,
             'darwin': None, 'pushbullet': None, 'pushover': None,
             'pushjet': None, 'telegram': None, 'win32': None,
             'xmpp': None}


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
            backend = backend_config.pop('backend')

        notifier = None
        notifier = notifiers.get(backend)
        if notifier is None:
            logging.getLogger(__name__).error(
                'Invalid backend {}'.format(backend))
            ret = 1
            continue

        try:
            notifier.notify(message=message, title=title, retcode=retcode,
                            **backend_config)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception as e:
            ret = 1
            if isinstance(e, DefaultNotifierError):
                notifier = e.module
                e = e.exception

            args, _, _, defaults = getargspec(notifier.notify)
            possible_args = set(args)
            required_args = set(args[:-len(defaults)])
            required_args -= set(['title', 'message', 'retcode'])
            unknown_args = set(backend_config) - possible_args
            missing_args = required_args - set(backend_config)

            if unknown_args:
                logging.getLogger(__name__).error(
                    'Got unknown arguments: {}'.format(unknown_args))

            if missing_args:
                logging.getLogger(__name__).error(
                    'Missing arguments: {}'.format(missing_args))

            if not any([unknown_args, missing_args]):
                logging.getLogger(__name__).error(
                    'Failed to send notification using {}'.format(backend),
                    exc_info=True)

    return ret
