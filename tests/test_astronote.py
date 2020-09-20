from unittest import TestCase, main

from mock import patch
from ntfy.backends.astronote import notify
from ntfy.config import USER_AGENT


class TestAstroNote(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', token='token')
        mock_post.assert_called_once_with(
            'https://api.astronote.app/1/notify',
            json={
                'body': 'message',
                'title': 'title',
            },
            headers={
                'Authorization': 'token token',
                'User-Agent': USER_AGENT,
            })

    @patch('requests.post')
    def test_persistent(self, mock_post):
        notify('title', 'message', token='token', persistent=False)
        mock_post.assert_called_once_with(
            'https://api.astronote.app/1/notify',
            json={
                'body': 'message',
                'title': 'title',
                'persistent': False,
            },
            headers={
                'Authorization': 'token token',
                'User-Agent': USER_AGENT,
            })

    @patch('requests.post')
    def test_category(self, mock_post):
        notify('title', 'message', token='token', category='category')
        mock_post.assert_called_once_with(
            'https://api.astronote.app/1/notify',
            json={
                'body': 'message',
                'title': 'title',
                'category': 'category',
            },
            headers={
                'Authorization': 'token token',
                'User-Agent': USER_AGENT,
            })

    @patch('requests.post')
    def test_display_category(self, mock_post):
        notify('title', 'message', token='token', display_category=True)
        mock_post.assert_called_once_with(
            'https://api.astronote.app/1/notify',
            json={
                'body': 'message',
                'title': 'title',
                'display_category': True,
            },
            headers={
                'Authorization': 'token token',
                'User-Agent': USER_AGENT,
            })

    @patch('requests.post')
    def test_sound(self, mock_post):
        notify('title', 'message', token='token', sound='silent')
        mock_post.assert_called_once_with(
            'https://api.astronote.app/1/notify',
            json={
                'body': 'message',
                'title': 'title',
                'sound': 'silent',
            },
            headers={
                'Authorization': 'token token',
                'User-Agent': USER_AGENT,
            })


if __name__ == '__main__':
    main()
