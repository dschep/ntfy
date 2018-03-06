import requests

from ..config import USER_AGENT

NTFY_API_KEY = '7fb59b2bedc4df26afa306d5dc54495b6394295a'
API_URL = 'https://api.prowlapp.com/publicapi/add'
MIN_PRIORITY = -2
MAX_PRIORITY = 2


def notify(title,
           message,
           api_key=NTFY_API_KEY,
           provider_key=None,
           priority=0,
           url=None,
           retcode=None):
    """
    Optional parameters:
        * ``api_key`` - use your own application token
        * ``provider_key`` - if you are whitelisted
        * ``priority``
        * ``url``
    """

    data = {
        'apikey': api_key,
        'application': 'ntfy',
        'event': title,
        'description': message,
    }

    if MIN_PRIORITY <= priority <= MAX_PRIORITY:
        data['priority'] = priority
    else:
        raise ValueError('priority must be an integer from {:d} to {:d}'
                         .format(MIN_PRIORITY, MAX_PRIORITY))

    if url is not None:
        data['url'] = url

    if provider_key is not None:
        data['providerkey'] = provider_key

    resp = requests.post(
        API_URL, data=data, headers={
            'User-Agent': USER_AGENT,
        })

    resp.raise_for_status()
