from sys import modules, version_info
from unittest import TestCase, main

from mock import MagicMock, mock_open, patch
from ntfy.cli import main as ntfy_main

py = version_info.major

builtin_module = '__builtin__' if py == 2 else 'builtins'


class TestIntegration(TestCase):
    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    @patch('ntfy.backends.pushover.requests.post')
    def test_pushover(self, mock_post, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['pushover'],
            'pushover': {
                'user_key': MagicMock()
            },
        }
        self.assertEqual(0, ntfy_main(['send', 'foobar']))

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    @patch('ntfy.backends.prowl.requests.post')
    def test_prowl(self, mock_post, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['prowl'],
            'prowl': {
                'apikey': MagicMock()
            },
        }
        ntfy_main(['send', 'foobar'])

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    @patch('ntfy.backends.pushbullet.requests.post')
    def test_pushbullet(self, mock_post, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['pushbullet'],
            'pushbullet': {
                'access_token': MagicMock()
            },
        }
        self.assertEqual(0, ntfy_main(['send', 'foobar']))

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    @patch('ntfy.backends.simplepush.requests.post')
    def test_simplepush(self, mock_post, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['simplepush'],
            'simplepush': {
                'key': MagicMock()
            },
        }
        self.assertEqual(0, ntfy_main(['send', 'foobar']))

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.backends.default.platform', 'linux')
    @patch('ntfy.config.safe_load')
    def test_default(self, mock_yamlload):
        old_dbus = modules.get('dbus')
        modules['dbus'] = MagicMock()
        try:
            mock_yamlload.return_value = {
                'backends': ['default'],
            }
            self.assertEqual(0, ntfy_main(['send', 'foobar']))
        finally:
            if old_dbus is not None:
                modules['dbus'] = old_dbus

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    def test_linux(self, mock_yamlload):
        old_dbus = modules.get('dbus')
        modules['dbus'] = MagicMock()
        try:
            mock_yamlload.return_value = {
                'backends': ['linux'],
            }
            self.assertEqual(0, ntfy_main(['send', 'foobar']))
        finally:
            if old_dbus is not None:
                modules['dbus'] = old_dbus

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    def test_darwin(self, mock_yamlload):
        old_foundation = modules.get('Foundation')
        old_objc = modules.get('objc')
        old_appkit = modules.get('AppKit')
        modules['Foundation'] = MagicMock()
        modules['objc'] = MagicMock()
        modules['AppKit'] = MagicMock()
        try:
            mock_yamlload.return_value = {
                'backends': ['darwin'],
            }
            self.assertEqual(0, ntfy_main(['send', 'foobar']))
        finally:
            if old_foundation is not None:
                modules['Foundation'] = old_foundation
            if old_objc is not None:
                modules['objc'] = old_objc
            if old_appkit is not None:
                modules['AppKit'] = old_appkit

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    def test_win32(self, mock_yamlload):
        old_win32api = modules.get('win32api')
        old_win32gui = modules.get('win32gui')
        old_win32con = modules.get('win32con')
        modules['win32api'] = MagicMock()
        modules['win32gui'] = MagicMock()
        modules['win32con'] = MagicMock()
        try:
            mock_yamlload.return_value = {
                'backends': ['win32'],
            }
            self.assertEqual(0, ntfy_main(['send', 'foobar']))
        finally:
            if old_win32api is not None:
                modules['win32api'] = old_win32api
            if old_win32gui is not None:
                modules['win32gui'] = old_win32gui
            if old_win32con is not None:
                modules['win32con'] = old_win32con

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    @patch('ntfy.backends.xmpp.NtfySendMsgBot')
    def test_xmpp(self, mock_bot, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['xmpp'],
            'xmpp': {
                'jid': 'foo@bar',
                'password': 'hunter2',
                'recipient': 'bar@foo'
            }
        }
        self.assertEqual(0, ntfy_main(['send', 'foobar']))

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    def test_instapush(self, mock_yamlload):
        modules['instapush'] = MagicMock()
        modules['instapush'].App().notify.return_value = {'status': 200}

        mock_yamlload.return_value = {
            'backends': ['insta'],
            'insta': {
                'appid': 'appid',
                'secret': 'secret',
                'event_name': 'event',
                'trackers': ['a']
            }
        }
        ntfy_main(['send', 'ms'])


if __name__ == '__main__':
    main()
