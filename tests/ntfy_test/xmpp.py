from unittest import TestCase
from mock import patch, MagicMock

from ntfy.backends.xmpp import NtfySendMsgBot
from ntfy.config import USER_AGENT


class NtfySendMsgBotTestCase(TestCase):
    @patch('sleekxmpp.ClientXMPP.add_event_handler')
    def test_eventhandler(self, mock_add_event_handler):
        bot = NtfySendMsgBot('foo@bar', 'hunter2', 'bar@foo', 'title',
                             'message')
        mock_add_event_handler.assert_called_with('session_start',
                                                  bot.start)

    @patch('sleekxmpp.ClientXMPP.send_presence')
    @patch('sleekxmpp.ClientXMPP.get_roster')
    @patch('sleekxmpp.ClientXMPP.disconnect')
    @patch('sleekxmpp.ClientXMPP.send_message')
    def test_start(self, mock_send_message, *other_mocks):
        bot = NtfySendMsgBot('foo@bar', 'hunter2', 'bar@foo', 'title',
                             'message')
        bot.start(MagicMock)
        mock_send_message.assert_called_with(mbody='message', msubject='title',
                                             mto='bar@foo')
