import requests
import json

from ..config import USER_AGENT

GOTIFY_MSG_URL = '{url}/message?token={token}'


def notify(title,
           message,
           url,
           access_token,
           extras=None,
           priority=None,
           retcode=None):
    """
    Required parameter:
        * ``url`` - The url of the gotify server
        * ``access_token`` - Your Gotify App access token

    Optional parameters:
        * ``extras`` - Additional data in json format sent along the message
        * ``priority`` - integer

    For more info, see: https://gotify.net/docs
    """

    data = {
        'title': title,
        'message': message,
    }

    if priority is not None:
        data['priority'] = priority

    if extras is not None:
        data['extras'] = json.load(extras)

    headers = {'User-Agent': USER_AGENT}

    resp = requests.post(GOTIFY_MSG_URL.format(url=url, token=access_token),
                         json=data,
                         headers=headers)

    resp.raise_for_status()
