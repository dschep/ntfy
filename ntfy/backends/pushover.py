import requests


def notify(title, message, user_key,
           api_token='aUnsraBiEZVsmrG89AZp47K3S2dX2a', device=None,
           sound=None, priority=0, expire=30,
           retry=30, callback=None, **kwargs):
    """
    Required config keys:
        * 'user_key'

    Optional config keys:
        * 'sound'
        * 'priority'
        * 'expire'
        * 'retry'
        * 'callback'
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

    if priority != 0 and priority <= 2 and priority >= -2:
        data['priority'] = priority

        # Expire, Retry, and Callback only apply to an Emergency Priority
        if priority == 2:
            # Retry can not be less than 30 per the API
            if retry < 30:
                data['retry'] = 30
            else:
                data['retry'] = retry

            data['expire'] = expire

            if callback:
                data['callback'] = callback

    resp = requests.post('https://api.pushover.net/1/messages.json',
                         data=data)

    resp.raise_for_status()
