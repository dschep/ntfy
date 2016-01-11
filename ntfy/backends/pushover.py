import requests


def notify(title, message, config, api_token, user_key, device=None, **kwargs):
    """
    Required config keys:
        * 'api_token'
        * 'user_key'
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
