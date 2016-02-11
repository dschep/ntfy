from unittest import TestCase, main
from mock import patch

from ntfy.backends.pushover import notify
from ntfy.config import USER_AGENT


class TestPushover(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', user_key='user_key')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title'},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_device(self, mock_post):
        notify('title', 'message', user_key='user_key', device='foobar')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title',
                  'device': 'foobar'},
            headers={'User-Agent': USER_AGENT})

if __name__ == '__main__':
    main()
