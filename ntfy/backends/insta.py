import logging
from instapush import App

class WrongMessageCountException(Exception):
    pass

class ApiException(Exception):
    pass

def notify(title, message, event_name, appid, secret, trackers, retcode=None):
    logger = logging.getLogger(__name__)
    msgs = message.split(":")

    if len(msgs) != len(trackers):
        logger.error("Wrong number of messages! There are {} trackers so you have to provide {} messages. Remember to separate eah message with ':' (example: send \"msg1:msg2\")".format(len(trackers), len(trackers)))
        raise WrongMessageCountException()

    to_send = {}

    for tracker, msg in zip(trackers, msgs):
        to_send[tracker] = msg

    app = App(appid=appid, secret=secret) 
    res = app.notify(event_name=event_name,trackers=to_send)

    if res["status"] != 200:
        logger.error(res["msg"])
        raise ApiException()