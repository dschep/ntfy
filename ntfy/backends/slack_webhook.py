import requests


def notify(title, message, url, user, **kwargs):

    requests.post(
        url,
        json={
            "username": "ntfy",
            "icon_url": "https://ntfy.readthedocs.io/en/latest/_static/logo.png",
            "text": "{0}\n{1}".format(title, message),
            "channel": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*{0}* {1}".format(title, message),
                    },
                }
            ],
        },
    )
