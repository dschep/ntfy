from unittest import TestCase

from mock import patch
from ntfy.backends.simplepush import notify
from ntfy.config import USER_AGENT


class TestSimplepush(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', key='secret')
        mock_post.assert_called_once_with(
            'https://api.simplepush.io/send',
            data={'title': 'title',
                  'msg': 'message',
                  'key': 'secret'},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_event(self, mock_post):
        notify('title', 'message', key='secret', event='foo')
        mock_post.assert_called_once_with(
            'https://api.simplepush.io/send',
            data={
                'title': 'title',
                'msg': 'message',
                'key': 'secret',
                'event': 'foo'
            },
            headers={'User-Agent': USER_AGENT})
