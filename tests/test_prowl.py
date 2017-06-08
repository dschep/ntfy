from unittest import TestCase, main

from mock import patch
from ntfy.backends.prowl import API_URL, NTFY_API_KEY, notify
from ntfy.config import USER_AGENT

TITLE = 'title'
MESSAGE = 'message'


class TestProwl(TestCase):
    def setUp(self):
        self.post_patcher = patch('requests.post')
        self.response_patcher = patch('requests.Response')
        self.mock_post = self.post_patcher.start()
        self.mock_response = self.response_patcher.start()
        self.mock_post.return_value = self.mock_response

    def tearDown(self):
        self.post_patcher.stop()
        self.response_patcher.stop()

    def verify_post(self, priority=0, **kwargs):
        data = {
            'apikey': NTFY_API_KEY,
            'event': TITLE,
            'description': MESSAGE,
            'application': 'ntfy',
            'priority': priority,
        }
        data.update(kwargs)
        self.mock_post.assert_called_once_with(
            API_URL, data=data, headers={'User-Agent': USER_AGENT})
        self.mock_response.raise_for_status.assert_called_once()

    def test_basic(self):
        notify(TITLE, MESSAGE)
        self.verify_post()

    def test_high_priority(self):
        notify(TITLE, MESSAGE, priority=2)
        self.verify_post(priority=2)

    def test_low_priority(self):
        notify(TITLE, MESSAGE, priority=-2)
        self.verify_post(priority=-2)

    def test_priority_too_high(self):
        self.assertRaises(ValueError, notify, TITLE, MESSAGE, priority=3)

    def test_priority_too_low(self):
        self.assertRaises(ValueError, notify, TITLE, MESSAGE, priority=-3)

    def test_url(self):
        notify(TITLE, MESSAGE, url='foobar')
        self.verify_post(url='foobar')

    def test_provider_key(self):
        notify(TITLE, MESSAGE, provider_key='providerkey')
        self.verify_post(providerkey='providerkey')


if __name__ == '__main__':
    main()
