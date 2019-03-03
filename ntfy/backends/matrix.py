from __future__ import unicode_literals
from matrix_client.client import MatrixClient

def notify(title, message, url, roomId, userId=None, token=None, password=None, retcode=None):

    client = MatrixClient(url)
    if password is not None:
        if userId is None:
            raise Exception("Must supply 'userid' when using 'password'")
        client.login(userId, password, sync=False)
    elif token is not None:
        client.api.token = token
    else:
        raise Exception("Must supply 'token' or 'password'")
    msg_plain = "**{}** {}".format(title, message)
    msg_html = "<b>{}</b> {}".format(title, message)
    room = client.join_room(roomId)
    room.send_html(msg_html, msg_plain)
