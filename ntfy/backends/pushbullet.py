import requests


def notify(title, message, config, device=None):
    """
    Required config keys:
        * 'access_token'
    """

    data = {
        'type': 'note',
        'title': title,
        'body': message,
    }
    if device is not None:
        data['device_iden'] = device

    headers = {'Access-Token': config['access_token']}

    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=data, headers=headers)

    resp.raise_for_status()
