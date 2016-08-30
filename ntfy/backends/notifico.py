import logging
import requests


def notify(title, message, retcode=None, webhook=None):
    logger = logging.getLogger(__name__)
    if webhook is None:
        logger.error(
            'please set webhook variable under '
            'notifico backend of the config file')
        return
    response = requests.get(webhook, params={
        'payload': '{title}\n{message}'.format(title=title, message=message)
    })
    response.raise_for_status()
