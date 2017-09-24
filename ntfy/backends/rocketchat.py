from rocketchat_API.rocketchat import RocketChat


def notify(title, message, url, username, password, room, retcode=None):

    rocket = RocketChat(username, password, server_url=url)

    msg = "**{}:** {}".format(title, message)
    rocket.chat_post_message(msg, channel=room)
