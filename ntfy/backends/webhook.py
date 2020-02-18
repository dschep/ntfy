from requests import Request


def notify(title, message, url):

    req = Request('POST', url, data={"text": message}, headers={"Content-type": "application/json"})