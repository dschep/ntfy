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
    def test_url_title(self, mock_post):
        notify('title', 'message', user_key='user_key',
               url_title='foo', url='bar')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title',
                  'url_title': 'foo', 'url': 'bar'},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_html(self, mock_post):
        notify('title', 'message', user_key='user_key', html=True)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title',
                  'html': 1},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_priority(self, mock_post):
        notify('title', 'message', user_key='user_key', priority=1)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title',
                  'priority': 1},
            headers={'User-Agent': USER_AGENT})

for option in ['device', 'sound', 'url']:
    @patch('requests.post')
    def test_option(self, mock_post):
        option_kwarg = {option: 'foobar'}
        notify('title', 'message', user_key='user_key', **option_kwarg)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key', 'message': 'message', 'token':
                  'aUnsraBiEZVsmrG89AZp47K3S2dX2a', 'title': 'title',
                  option: 'foobar'},
            headers={'User-Agent': USER_AGENT})
    setattr(TestPushover, 'test_{}'.format(option), test_option)

if __name__ == '__main__':
    main()
