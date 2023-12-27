import requests


def notify(title, message, url, user_id, auth_token, channel, **kwargs):
    requests.post(
        url,
        headers={
            "X-Auth-Token": auth_token,
            "X-User-Id": user_id,
        },
        json={
            "text": "{0}\n{1}".format(title, message),
            "channel": channel,
        },
    )
