import requests


def notify(title, message, access_token, device_iden=None, email=None, **kwargs):
    """
    Required config keys:
        * 'access_token'
    """

    data = {
        'type': 'note',
        'title': title,
        'body': message,
    }
    if device_iden is not None:
        data['device_iden'] = device_iden
    if email is not None:
        data['email'] = email

    headers = {'Access-Token': access_token}

    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=data, headers=headers)

    resp.raise_for_status()
