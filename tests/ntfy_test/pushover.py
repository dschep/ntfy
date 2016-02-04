from unittest import TestCase, main
from mock import patch

from ntfy.backends.pushover import notify


class TestPushover(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        notify('title', 'message', user_key='user_key')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title'})

    @patch('requests.post')
    def test_device(self, mock_post):
        notify('title', 'message', user_key='user_key', device='foobar')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title',
                  'device': 'foobar'})

if __name__ == '__main__':
    main()
