from unittest import TestCase

from mock import patch
from ntfy.backends.pushjet import notify
from ntfy.config import USER_AGENT


class TestPushjet(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', secret='secret')
        mock_post.assert_called_once_with(
            'https://api.pushjet.io/message',
            data={
                'title': 'title',
                'message': 'message',
                'secret': 'secret',
                'level': 3
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_link(self, mock_post):
        notify('title', 'message', secret='secret', link='foobar')
        mock_post.assert_called_once_with(
            'https://api.pushjet.io/message',
            data={
                'title': 'title',
                'message': 'message',
                'secret': 'secret',
                'level': 3,
                'link': 'foobar'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_endpoint(self, mock_post):
        notify('title', 'message', secret='secret', endpoint='http://foobar')
        mock_post.assert_called_once_with(
            'http://foobar/message',
            data={
                'title': 'title',
                'message': 'message',
                'secret': 'secret',
                'level': 3
            },
            headers={'User-Agent': USER_AGENT})
