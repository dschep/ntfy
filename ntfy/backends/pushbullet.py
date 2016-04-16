import requests

from ..config import USER_AGENT


def notify(title,
           message,
           access_token,
           device_iden=None,
           email=None,
           **kwargs):
    """
    Required parameter:
        * ``access_token`` - Your Pushbullet access token, created at
            https://www.pushbullet.com/#settings/account

    Optional parameters:
        * ``device_iden`` - a device identifier, if omited, notification is
                            sent to all devices
        * ``email`` - send notification to pushbullte user with the specified
                      email or send an email if they aren't a pushullet user
    """

    data = {'type': 'note', 'title': title, 'body': message, }
    if device_iden is not None:
        data['device_iden'] = device_iden
    if email is not None:
        data['email'] = email

    headers = {'Access-Token': access_token, 'User-Agent': USER_AGENT}

    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=data,
                         headers=headers)

    resp.raise_for_status()
