import requests


def notify(title,
           message,
           topic,
           base_url='https://ntfy.sh',
           retcode=None):
    resp = requests.post(f"{base_url}/{topic}", data=message)
    resp.raise_for_status()
