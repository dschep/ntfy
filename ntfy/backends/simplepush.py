import requests
from simplepush import generate_payload

from ..config import USER_AGENT


def notify(title,
           message,
           key,
           event=None,
           password=None,
           retcode=None):
    """
    Required paramter:
        * ``key`` - The Simplepush identification key, created by
        installing the Android App (https://simplepush.io)

    Optional parameters:
        * ``password`` - password for end-to-end encryption (can
        be set in the app)
        * ``event`` - use custom ringtones and vibration patterns
    """

    data = generate_payload(key, title if len(title) <= 200 else title[:199] + u'\u2026', message, event, password)

    headers = {'User-Agent': USER_AGENT}

    endpoint = "https://api.simplepush.io"

    resp = requests.post(endpoint + '/send',
                         data=data,
                         headers=headers)

    resp.raise_for_status()
