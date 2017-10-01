import logging
import re

from instapush import App


class WrongMessageCountException(Exception):
    pass


class ApiException(Exception):
    pass


def notify(title, message, event_name, appid, secret, trackers, retcode=None):
    """
    Required parameter:
        * ``event_name`` - Instapush event (the notification template)
        * ``appid`` - The appid found on the dashboard
        * ``secret`` - The secret found on the dashboard
        * ``traskers`` - List of the placeholders for the selected event
    """

    logger = logging.getLogger(__name__)
    _msgs = re.split(r'(?<!\\):', message)
    msgs = []

    for msg in _msgs:
        msg = msg.replace("\\:", ":")
        msgs.append(msg)

    if len(msgs) != len(trackers):
        logger.error(('Wrong number of messages! There are {} trackers so you '
                      'have to provide {} messages. Remember to separate each '
                      'message with \':\' (example: send "msg1:msg2")').format(
                          len(trackers), len(trackers)))
        raise WrongMessageCountException()

    to_send = {}

    for tracker, msg in zip(trackers, msgs):
        to_send[tracker] = msg

    app = App(appid=appid, secret=secret)
    res = app.notify(event_name=event_name, trackers=to_send)

    if res["status"] != 200:
        logger.error(res["msg"])
        raise ApiException()
