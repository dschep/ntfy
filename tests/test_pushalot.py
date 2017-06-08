from unittest import TestCase, main

from mock import patch
from ntfy.backends.pushalot import notify
from ntfy.config import USER_AGENT


class TestPushalot(TestCase):
    URL = 'https://pushalot.com/api/sendmessage'

    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_silent(self, mock_post):
        notify('title', 'message', silent=True, auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'IsSilent': 'True',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_important(self, mock_post):
        notify('title', 'message', important=True, auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'IsImportant': 'True',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_source(self, mock_post):
        notify('title', 'message', source='source', auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'Source': 'source',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_url(self, mock_post):
        notify(
            'title', 'message', url='example.com', auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'Link': 'example.com',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_url_title(self, mock_post):
        notify(
            'title',
            'message',
            url='example.com',
            url_title='url title',
            auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'Link': 'example.com',
                'LinkTitle': 'url title',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_image(self, mock_post):
        notify(
            'title', 'message', image='image.jpg', auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'Image': 'image.jpg',
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_ttl(self, mock_post):
        notify('title', 'message', ttl=100, auth_token='access_token')
        mock_post.assert_called_once_with(
            self.URL,
            data={
                'Body': 'message',
                'Title': 'title',
                'TimeToLive': 100,
                'AuthorizationToken': 'access_token'
            },
            headers={'User-Agent': USER_AGENT})


if __name__ == '__main__':
    main()
