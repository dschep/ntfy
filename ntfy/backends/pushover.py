import requests


def notify(message, config, subject=None, device=None):
    """
    Required config keys:
        * 'api_token'
        * 'user_key'
    """

    data = {
        'message': message,
        'token': config['api_token'],
        'user': config['user_key']
    }
    if subject:
        data['title'] = subject
    if device:
        data['device'] = device

    resp = requests.post('https://api.pushover.net/1/messages.json',
                         data=data)

    resp.raise_for_status()
