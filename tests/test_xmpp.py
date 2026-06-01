from unittest import TestCase

from unittest.mock import MagicMock, patch, AsyncMock
from ntfy.backends.xmpp import NtfySendMsgBot, notify
from ntfy.config import USER_AGENT


class NtfySendMsgBotTestCase(TestCase):
    @patch('slixmpp.ClientXMPP.add_event_handler')
    def test_eventhandler(self, mock_add_event_handler):
        bot = NtfySendMsgBot('foo@bar', 'hunter2', 'bar@foo', 'title',
                             'message')
        mock_add_event_handler.assert_called_with('session_start', bot.start)

    @patch('slixmpp.ClientXMPP.send_presence')
    @patch('slixmpp.ClientXMPP.get_roster', new_callable=AsyncMock)
    @patch('slixmpp.ClientXMPP.disconnect')
    @patch('slixmpp.ClientXMPP.send_message')
    def test_start(self, mock_send_message, *other_mocks):
        bot = NtfySendMsgBot('foo@bar', 'hunter2', 'bar@foo', 'title',
                             'message')
        import asyncio
        asyncio.run(bot.start(MagicMock()))
        mock_send_message.assert_called_with(
            mbody='message', msubject='title', mto='bar@foo')

    @patch('slixmpp.ClientXMPP.send_presence')
    @patch('slixmpp.ClientXMPP.get_roster', new_callable=AsyncMock)
    @patch('slixmpp.ClientXMPP.disconnect')
    @patch('slixmpp.ClientXMPP.send_message')
    def test_start_mtype(self, mock_send_message, *other_mocks):
        bot = NtfySendMsgBot(
            'foo@bar', 'hunter2', 'bar@foo', 'title', 'message', mtype='chat')
        import asyncio
        asyncio.run(bot.start(MagicMock()))
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
