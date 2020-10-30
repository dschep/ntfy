import requests


def notify(title, message, url, user, **kwargs):

    requests.post(
        url,
        json={
            "text": "{0}\n{1}".format(title, message),
            "user": user,
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
