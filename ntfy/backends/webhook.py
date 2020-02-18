import requests


def notify(title, message, url, retcode=None):

    requests.post(url, json={"text": "*{}*\n{}".format(title, message)})
