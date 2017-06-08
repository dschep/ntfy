from unittest import TestCase

from mock import MagicMock, patch
from ntfy.backends.xmpp import NtfySendMsgBot, notify
from ntfy.config import USER_AGENT


class NtfySendMsgBotTestCase(TestCase):
    @patch('sleekxmpp.ClientXMPP.add_event_handler')
    def test_eventhandler(self, mock_add_event_handler):
        bot = NtfySendMsgBot('foo@bar', 'hunter2', 'bar@foo', 'title',
                             'message')
        mock_add_event_handler.assert_called_with('session_start', bot.start)

    @patch('sleekxmpp.ClientXMPP.send_presence')
    @patch('sleekxmpp.ClientXMPP.get_roster')
    @patch('sleekxmpp.ClientXMPP.disconnect')
    @patch('sleekxmpp.ClientXMPP.send_message')
    def test_start(self, mock_send_message, *other_mocks):
        bot = NtfySendMsgBot('foo@bar', 'hunter2', 'bar@foo', 'title',
                             'message')
        bot.start(MagicMock)
        mock_send_message.assert_called_with(
            mbody='message', msubject='title', mto='bar@foo')

    @patch('sleekxmpp.ClientXMPP.send_presence')
    @patch('sleekxmpp.ClientXMPP.get_roster')
    @patch('sleekxmpp.ClientXMPP.disconnect')
    @patch('sleekxmpp.ClientXMPP.send_message')
    def test_start_mtype(self, mock_send_message, *other_mocks):
        bot = NtfySendMsgBot(
            'foo@bar', 'hunter2', 'bar@foo', 'title', 'message', mtype='chat')
        bot.start(MagicMock)
        mock_send_message.assert_called_with(
            mbody='message', msubject='title', mto='bar@foo', mtype='chat')


class XMPPTestCase(TestCase):
    @patch('os.path.isdir')
    @patch('ntfy.backends.xmpp.NtfySendMsgBot')
    def test_capath(self, mock_bot_class, mock_isdir):
        notify(
            'title',
            'message',
            'foo@bar',
            'hunter2',
            'bar@foo',
            path_to_certs='/custom/ca')
        self.assertEqual('/custom/ca', mock_bot_class().ca_certs)
