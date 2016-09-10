from slacker import Slacker


def notify(title, message, token, recipient, retcode=None):

    slack = Slacker(token)

    slack.chat.post_message(recipient, message)
