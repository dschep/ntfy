import requests


def notify(title, message, user_key,
           api_token='aUnsraBiEZVsmrG89AZp47K3S2dX2a', device=None, **kwargs):
    """
    Required parameters:
        * ``user_key``

    Optional parameters
        * ``access_token`` - use your own application token
        * ``device`` - target a device, if omitted, notification is sent to all devices
    """

    data = {
        'message': message,
        'token': api_token,
        'user': user_key,
        'title': title,
    }
    if device:
        data['device'] = device

    resp = requests.post('https://api.pushover.net/1/messages.json',
                         data=data)

    resp.raise_for_status()
