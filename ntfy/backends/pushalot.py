import requests

from ..config import USER_AGENT

# URL to pushalot.com notification sending endpoint
PUSHALOT_API_URL = 'https://pushalot.com/api/sendmessage'


def notify(title,
           message,
           auth_token,
           source=None,
           url=None,
           url_title=None,
           image=None,
           ttl=None,
           important=False,
           silent=False,
           retcode=None):
    """
    Required parameters:
        * ``auth_token``

    Optional parameters:
        * ``source``
        * ``url``
        * ``url_title``
        * ``image``
        * ``ttl``
        * ``important``
        * ``silent``
    """

    data = {
        'Title': title,
        'Body': message,
        'AuthorizationToken': auth_token,
    }

    if source:
        data['Source'] = source
    if url:
        data['Link'] = url
    if url and url_title:
        data['LinkTitle'] = url_title
    if image:
        data['Image'] = image
    if ttl:
        data['TimeToLive'] = int(ttl)
    if important:
        data['IsImportant'] = 'True'
    if silent:
        data['IsSilent'] = 'True'

    headers = {'User-Agent': USER_AGENT}
    response = requests.post(PUSHALOT_API_URL, data=data, headers=headers)
    response.raise_for_status()
