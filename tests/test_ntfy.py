from unittest import TestCase

from mock import patch

from ntfy import notify
import ntfy

class DummyModule:

    def notify(message, title, retcode):
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

    @patch('ntfy.notifiers', {'default': DummyModule})
    def test_backenderror(self):
        ret = ntfy.notify('message', 'title')
        self.assertEqual(ret, 1)
