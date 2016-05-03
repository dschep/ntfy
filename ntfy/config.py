import errno
import logging
from os.path import expanduser
from os.path import join as join_path
from sys import exit

from ruamel import yaml
import requests
from appdirs import site_config_dir, user_config_dir

from . import __version__

DEFAULT_CONFIG = join_path(user_config_dir('ntfy', 'dschep'), 'ntfy.yml')
SITE_DEFAULT_CONFIG = join_path(site_config_dir('ntfy', 'dschep'), 'ntfy.yml')
OLD_DEFAULT_CONFIG = expanduser('~/.ntfy.yml')

USER_AGENT = 'ntfy/{version} {default_user_agent}'.format(
    version=__version__,
    default_user_agent=requests.utils.default_user_agent())


def load_config(config_path=DEFAULT_CONFIG):
    logger = logging.getLogger(__name__)

    try:
        config = yaml.load(open(expanduser(config_path)))
    except IOError as e:
        if e.errno == errno.ENOENT and config_path == DEFAULT_CONFIG:
            logger.info('{} not found'.format(config_path))
            config = {}
        else:
            logger.error('Failed to open {}'.format(config_path),
                         exc_info=True)
            exit(1)
    except ValueError as e:
        logger.error('Failed to load {}'.format(config_path), exc_info=True)
        exit(1)

    if 'backend' in config:
        logger.warning(
            "The 'backend' config option is deprecated, use 'backends'")
        if 'backends' in config:
            logger.warning("Both 'backend' and 'backends' in config, "
                           "ignoring 'backend'.")
        else:
            config['backends'] = [config['backend']]

    return config
