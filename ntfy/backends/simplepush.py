import requests

from ..config import USER_AGENT

def notify(title,
           message,
           key):
    """
    Required paramter:
        * ``key`` - The Simplepush identification key, created by
        installing the Android App (https://simplepush.io)
    """

    data = {
        'title': title,
        'msg': message,
        'key': key
    }

    headers = {'User-Agent': USER_AGENT}

    endpoint = "https://api.simplepush.io"

    resp = requests.post(endpoint + '/send',
                         data=data,
                         headers=headers)

    resp.raise_for_status()
