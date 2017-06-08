from unittest import TestCase, main

from mock import patch
from ntfy.backends.pushbullet import notify
from ntfy.config import USER_AGENT


class TestPushbullet(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', access_token='access_token')
        mock_post.assert_called_once_with(
            'https://api.pushbullet.com/v2/pushes',
            data={'body': 'message',
                  'title': 'title',
                  'type': 'note'},
            headers={'Access-Token': 'access_token',
                     'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_device(self, mock_post):
        notify(
            'title',
            'message',
            access_token='access_token',
            device_iden='foobar')
        mock_post.assert_called_once_with(
            'https://api.pushbullet.com/v2/pushes',
            data={
                'body': 'message',
                'title': 'title',
                'device_iden': 'foobar',
                'type': 'note'
            },
            headers={'Access-Token': 'access_token',
                     'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_email(self, mock_post):
        notify(
            'title',
            'message',
            access_token='access_token',
            email='foobar@example.com')
        mock_post.assert_called_once_with(
            'https://api.pushbullet.com/v2/pushes',
            data={
                'body': 'message',
                'title': 'title',
                'email': 'foobar@example.com',
                'type': 'note'
            },
            headers={'Access-Token': 'access_token',
                     'User-Agent': USER_AGENT})


if __name__ == '__main__':
    main()
