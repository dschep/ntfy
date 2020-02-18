import requests


def notify(title, message, url, retcode=None):

    req = requests.post(url, json={"text": "*{}*: {}".format(title,message)})