from slacker import Slacker


def notify(title, message, token, recipient, retcode=None, **kwargs):
    kwargs.setdefault("username", title)

    slack = Slacker(token)

    slack.chat.post_message(recipient, message, **kwargs)
