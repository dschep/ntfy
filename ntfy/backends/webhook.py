import requests
from ..config import USER_AGENT


def notify(title, message, url, verify=True, retcode=None):

    payload = {"text": "*{}*\n{}".format(title, message)}
    headers = {'User-Agent': USER_AGENT}

    response = requests.post(url, json=payload, headers=headers, verify=verify)
    response.raise_for_status()
