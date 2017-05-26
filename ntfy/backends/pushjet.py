import requests

from ..config import USER_AGENT


def notify(title,
           message,
           secret,
           endpoint=None,
           level=3,
           link=None,
           retcode=None):
    """
    Required parameter:
        * ``secret`` - The Pushjet service secret token, created with
            http://docs.pushjet.io/docs/creating-a-new-service

    Optional parameters:
        * ``endpoint`` - custom Pushjet API endpoint
            (defaults to https://api.pushjet.io)
        * ``level`` - The importance level from 1(low) to 5(high)
        * ``link``
    """

    data = {
        'title': title,
        'message': message,
        'level': level,
        'secret': secret,
    }

    if link:
        data['link'] = link

    headers = {'User-Agent': USER_AGENT}

    if endpoint is None:
        endpoint = 'https://api.pushjet.io'

    resp = requests.post(endpoint + '/message', data=data, headers=headers)

    resp.raise_for_status()
