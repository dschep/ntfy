from slacker import Slacker


def notify(title, message, token, user, retcode=None):

    slack = Slacker(token)

    user_str = '@{}'.format(user)
    slack.chat.post_message(user_str, message)
