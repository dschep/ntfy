from unittest import TestCase

from mock import patch
from ntfy.backends.webhook import notify
from ntfy.config import USER_AGENT


class TestWebhook(TestCase):
    @patch('requests.post')
    def test_basic(self, mock_post):
        url = 'https://hooks.slack.com/services/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'
        notify('title', 'message', url)
        mock_post.assert_called_once_with(
            url,
            json={'text': '*{}*\n{}'.format('title', 'message')},
            headers={'User-Agent': USER_AGENT})
