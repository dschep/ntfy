from unittest import TestCase

from mock import patch

from ntfy import notify

from . import cli


class OverrideBackendTestCase(TestCase):
    @patch('requests.post')
    def test_runcmd(self, mock_post):
        ret = notify('message', 'title', {
            'backends': ['foobar'],
            'foobar': {
                'backend': 'pushover',
                'user_key': 't0k3n',
            }
        })
        self.assertEqual(ret, 0)


class ErrorTestCase(TestCase):
    def test_invalidbackend(self):
        ret = notify('message', 'title', {'backends': ['foobar']})
        self.assertEqual(ret, 1)

    @patch('ntfy.backends.default.notify')
    def test_backenderror(self, mock_default_notify):
        mock_default_notify.side_effect = Exception
        ret = notify('message', 'title')
        self.assertEqual(ret, 1)
