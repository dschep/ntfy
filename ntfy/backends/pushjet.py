import requests

from ..config import USER_AGENT


def notify(title,
           message,
           secret,
           level=3,
           link=None,
           retcode=None):
    """
    Required parameter:
        * ``secret`` - The Pushjet service secret token, created with
            http://docs.pushjet.io/docs/creating-a-new-service

    Optional parameters:
        * ``level`` - The importance level from 1(low) to 5(high)
        * ``url``
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

    resp = requests.post('https://api.pushjet.io/message',
                         data=data,
                         headers=headers)

    resp.raise_for_status()
