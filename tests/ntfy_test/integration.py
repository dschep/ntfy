from unittest import TestCase, main
from sys import version_info, modules

from mock import patch, mock_open, MagicMock

from ntfy.cli import main as ntfy_main


py = version_info.major

class TestIntegration(TestCase):
    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    @patch('ntfy.backends.pushover.requests.post')
    def test_pushover(self, mock_post, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['pushover'],
            'pushover': {'user_key': MagicMock()},
        }
        ntfy_main(['send', 'foobar'])

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    @patch('ntfy.backends.pushbullet.requests.post')
    def test_pushbullet(self, mock_post, mock_yamlload):
        mock_yamlload.return_value = {
            'backends': ['pushbullet'],
            'pushbullet': {'access_token': MagicMock()},
        }
        ntfy_main(['send', 'foobar'])

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.backends.default.platform', 'linux')
    @patch('ntfy.config.yaml.load')
    def test_default(self, mock_yamlload):
        old_dbus = modules.get('dbus')
        modules['dbus'] = MagicMock()
        try:
            mock_yamlload.return_value = {
                'backends': ['default'],
            }
            ntfy_main(['send', 'foobar'])
        finally:
            if old_dbus is not None:
                modules['dbus'] = old_dbus

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    def test_linux(self, mock_yamlload):
        old_dbus = modules.get('dbus')
        modules['dbus'] = MagicMock()
        try:
            mock_yamlload.return_value = {
                'backends': ['linux'],
            }
            ntfy_main(['send', 'foobar'])
        finally:
            if old_dbus is not None:
                modules['dbus'] = old_dbus

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
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
            ntfy_main(['send', 'foobar'])
        finally:
            if old_foundation is not None:
                modules['Foundation'] = old_foundation
            if old_objc is not None:
                modules['objc'] = old_objc
            if old_appkit is not None:
                modules['AppKit'] = old_appkit

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
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
            ntfy_main(['send', 'foobar'])
        finally:
            if old_win32api is not None:
                modules['win32api'] = old_win32api
            if old_win32gui is not None:
                modules['win32gui'] = old_win32gui
            if old_win32con is not None:
                modules['win32con'] = old_win32con

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    @patch('ntfy.backends.xmpp.NtfySendMsgBot')
    def test_xmpp(self, mock_bot, mock_yamlload):
        mock_yamlload.return_value = {'backends': ['xmpp'],
                                      'xmpp': {'jid': 'foo@bar',
                                               'password': 'hunter2',
                                               'recipient': 'bar@foo'}}
        ntfy_main(['send', 'foobar'])


if __name__ == '__main__':
    main()
