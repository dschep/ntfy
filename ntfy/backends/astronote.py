from __future__ import print_function

import logging

import requests

from ..config import USER_AGENT


def notify(title,
           message,
           token=None,
           category=None,
           display_category=None,
           persistent=None,
           sound=None,
           retcode=None):
    """
    Required parameters:
        * ``token``

    Optional parameters:
        * ``category``
        * ``display_category``
        * ``persistent``
        * ``sound``
    """

    data = {
        'body': message,
        'title': title,
    }

    if category:
        data['category'] = category

    if display_category is not None:
        data['display_category'] = display_category

    if persistent is not None:
        data['persistent'] = persistent

    if sound:
        data['sound'] = sound

    resp = requests.post(
        'https://api.astronote.app/1/notify',
        json=data,
        headers={
            'Authorization': 'token %s' % token,
            'User-Agent': USER_AGENT,
        })

    resp.raise_for_status()
