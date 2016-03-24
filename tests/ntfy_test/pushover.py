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
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title'},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_url_title(self, mock_post):
        notify('title',
               'message',
               user_key='user_key',
               url_title='foo',
               url='bar')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'url_title': 'foo',
                  'url': 'bar'},
            headers={'User-Agent': USER_AGENT})

        mock_post.reset_mock()
        notify('title', 'message', user_key='user_key', url_title='foo')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title'},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_html(self, mock_post):
        notify('title', 'message', user_key='user_key', html=True)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'html': 1},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_priority(self, mock_post):
        notify('title', 'message', user_key='user_key', priority=1)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'priority': 1},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_invalid_priority(self, mock_post):
        self.assertRaises(ValueError,
                          notify,
                          'title',
                          'message',
                          user_key='user_key',
                          priority=3)

    @patch('requests.post')
    def test_hi_priority(self, mock_post):
        notify('title', 'message', user_key='user_key', priority=2)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'priority': 2,
                  'retry': 30,
                  'expire': 86400},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_hi_priority_retry(self, mock_post):
        notify('title', 'message', user_key='user_key', priority=2, retry=60)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'priority': 2,
                  'retry': 60,
                  'expire': 86400},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_hi_priority_expire(self, mock_post):
        notify('title', 'message', user_key='user_key', priority=2, expire=60)
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'priority': 2,
                  'retry': 30,
                  'expire': 60},
            headers={'User-Agent': USER_AGENT})

    @patch('requests.post')
    def test_hi_priority_callback(self, mock_post):
        notify('title',
               'message',
               user_key='user_key',
               priority=2,
               callback='http://example.com')
        mock_post.assert_called_once_with(
            'https://api.pushover.net/1/messages.json',
            data={'user': 'user_key',
                  'message': 'message',
                  'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                  'title': 'title',
                  'priority': 2,
                  'retry': 30,
                  'expire': 86400,
                  'callback': 'http://example.com'},
            headers={'User-Agent': USER_AGENT})


for option in ['device', 'sound', 'url']:

    def closure():
        @patch('requests.post')
        def test_option(self, mock_post):
            option_kwarg = {option: 'foobar'}
            notify('title', 'message', user_key='user_key', **option_kwarg)
            mock_post.assert_called_once_with(
                'https://api.pushover.net/1/messages.json',
                data={'user': 'user_key',
                      'message': 'message',
                      'token': 'aUnsraBiEZVsmrG89AZp47K3S2dX2a',
                      'title': 'title',
                      option: 'foobar'},
                headers={'User-Agent': USER_AGENT})

        setattr(TestPushover, 'test_{}'.format(option), test_option)

    closure()

if __name__ == '__main__':
    main()
