import asyncio
import logging
import os

import slixmpp


class NtfySendMsgBot(slixmpp.ClientXMPP):
    """
    Updated from sleekxmpp to slixmpp (async-based XMPP library).

    NOTE: supplying mtype='chat' was required for
          Google Hangouts to work
    """

    def __init__(self, jid, password, recipient, title, message, mtype=None):
        super().__init__(jid, password)

        self.recipient = recipient
        self.title = title
        self.msg = message
        self.mtype = mtype

        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        msg_args = {
            'mto': self.recipient,
            'msubject': self.title,
            'mbody': self.msg
        }
        if self.mtype:
            msg_args['mtype'] = self.mtype

        self.send_message(**msg_args)

        self.disconnect()


def notify(title,
           message,
           jid,
           password,
           recipient,
           hostname=None,
           port=5222,
           path_to_certs=None,
           mtype=None,
           retcode=None):
    """
    Optional parameters
        * ``hostname`` (if not from jid)
        * ``port``
        * ``path_to_certs``
        * ``mtype`` ('chat' required for Google Hangouts)

    To verify the SSL certificates offered by a server:
    path_to_certs = "path/to/ca/cert"

    Without dnspython library installed, you will need
    to specify the server hostname if it doesn't match the jid.

    For example, to use Google Talk you would need to use:
    hostname = 'talk.google.com'

    Specify port if other than 5222.
    NOTE: Ignored without specified hostname
    """

    xmpp_bot = NtfySendMsgBot(jid, password, recipient, title, message, mtype)

    if path_to_certs and os.path.isdir(path_to_certs):
        xmpp_bot.ca_certs = path_to_certs

    if hostname:
        xmpp_bot.connect((hostname, int(port)))
    else:
        xmpp_bot.connect()

    xmpp_bot.process()
