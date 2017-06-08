from unittest import TestCase

import ntfy
from mock import patch
from ntfy import notify


def mock_notify(message, title, retcode=None):
    raise Exception


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

    @patch('ntfy.backends.default.notify', mock_notify)
    def test_backenderror(self):
        ret = ntfy.notify('message', 'title')
        self.assertEqual(ret, 1)
