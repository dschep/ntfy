from slack_sdk import WebClient


def notify(title, message, token, recipient, retcode=None):

    slack = WebClient(token=token)

    slack.chat_postMessage(channel=recipient, text=message)
