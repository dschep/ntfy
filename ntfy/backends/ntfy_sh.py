import requests


def notify(title, message, topic, host='https://ntfy.sh', user=None, password=None, **kwargs):
    auth_kwarg = {'auth': (user, password)} if user and password else {}

    requests.post(
        f"{host}/{topic}",
        headers=dict(title=title),
        data=message,
        **auth_kwarg,
    )
