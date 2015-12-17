import requests


def notify(subject, config, message=None, device=None):
    data = {
        'type': 'note',
        'title': subject,
    }
    if message is not None:
        data['body'] = message
    if device is not None:
        data['device_iden'] = device

    headers = {'Access-Token': config['access_token']}

    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=data, headers=headers)

    resp.raise_for_status()
