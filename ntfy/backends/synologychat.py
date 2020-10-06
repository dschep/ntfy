import json
import warnings

import requests
import urllib3.exceptions

def notify(title, message,
           webhook_url, verify=True,
           retcode=None):

    body = 'payload=' + json.dumps({
        'text': message
    })

    if verify:
        response = requests.post(webhook_url, body)
    else:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(webhook_url, body, verify=False)

    response.raise_for_status()

    resp_body = response.json()
    if not resp_body['success']:
        print(response.text)
        return 1
