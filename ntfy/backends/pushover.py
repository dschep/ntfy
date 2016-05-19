import requests
import logging

from ..config import USER_AGENT


def notify(title,
           message,
           user_key,
           api_token='aUnsraBiEZVsmrG89AZp47K3S2dX2a',
           device=None,
           sound=None,
           priority=0,
           expire=None,
           retry=None,
           callback=None,
           url=None,
           url_title=None,
           html=False,
           **kwargs):
    """
    Required parameters:
        * ``user_key``

    Optional parameters:
        * ``sound``
        * ``priority``
        * ``expire``
        * ``retry``
        * ``callback``
        * ``access_token`` - use your own application token
        * ``device`` - target a device, if omitted, target all devices
        * ``url``
        * ``url_title``
        * ``html``
    """

    data = {
        'message': message,
        'token': api_token,
        'user': user_key,
        'title': title,
    }
    if device:
        data['device'] = device

    if sound:
        data['sound'] = sound

    if url:
        data['url'] = url

    if url_title:
        if not url:
            logging.getLogger(__name__).warning(
                'url_title specified without specifying url')
        else:
            data['url_title'] = url_title

    if html:
        data['html'] = 1

    priority = int(priority)
    if priority <= 2 and priority >= -2:
        if priority != 0:
            data['priority'] = priority

        # Expire, Retry, and Callback only apply to an Emergency Priority
        if priority == 2:
            # Retry can not be less than 30 per the API
            if not retry or retry < 30:
                logging.getLogger(
                    __name__).error('retry is less than 30 or is not set, '
                                    'setting retry to 30 to comply with '
                                    'pushover API requirements')
                data['retry'] = 30
            else:
                data['retry'] = retry

            # Expire can not be more than 86400 (24 hours)
            if not expire or expire > 86400:
                logging.getLogger(__name__).error(
                    'expire is greater than 86400 seconds or is not set,'
                    'setting expire to 86400 to comply with'
                    'pushover API requirements')
                data['expire'] = 86400
            elif expire <= 86400:
                data['expire'] = expire

            if callback:
                data['callback'] = callback
        else:
            if retry:
                logging.getLogger(__name__).warning(
                    'Non-emergency, ignoring retry set in config')
            if expire:
                logging.getLogger(__name__).warning(
                    'Non-emergency, ignoring expire set in config')
            if callback:
                logging.getLogger(__name__).warning(
                    'Non-emergency, ignoring callback set in config')

    else:
        raise ValueError('priority must be an integer from -2 to 2')

    resp = requests.post('https://api.pushover.net/1/messages.json',
                         data=data,
                         headers={'User-Agent': USER_AGENT})

    resp.raise_for_status()
