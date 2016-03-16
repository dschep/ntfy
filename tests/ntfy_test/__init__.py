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
