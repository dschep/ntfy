import logging
from getpass import getuser
from os import getcwd, path, name
from socket import gethostname
from importlib import import_module
from inspect import getargspec
from .backends.default import DefaultNotifierError

__version__ = '2.5.1'

_user_home = path.expanduser('~')
_cwd = getcwd()
if name != 'nt' and _cwd.startswith(_user_home):
    default_title = '{}@{}:{}'.format(getuser(), gethostname(),
                                      path.join('~',
                                                _cwd[len(_user_home) + 1:]))
else:
    default_title = '{}@{}:{}'.format(getuser(), gethostname(), _cwd)


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

        if title is None:
            title = backend_config.pop('title',
                                       config.get('title', default_title))
        elif 'title' in backend_config:
            del backend_config['title']

        try:
            notifier = import_module('ntfy.backends.{}'.format(backend))
        except ImportError:
            logging.getLogger(__name__).error(
                'Invalid backend {}'.format(backend))
            ret = 1
            continue

        try:
            notify_ret = notifier.notify(
                message=message,
                title=title,
                retcode=retcode,
                **backend_config)
            if notify_ret:
                ret = notify_ret
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
