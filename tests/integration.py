from os import devnull
from unittest import TestCase, main

from mock import patch, mock_open, MagicMock

from ntfy.cli import main as ntfy_main


class TestIntegration(TestCase):
    @patch('__builtin__.open', mock_open())
    @patch('ntfy.cli.json.load')
    @patch('ntfy.backends.pushover.requests.post')
    def test_pushover(self, mock_jsonload, mock_post):
        mock_jsonload.return_value = {
            'backends': ['pushover'],
            'pushover': {'user_key': MagicMock()},
        }
        ntfy_main(['send', 'foobar'])


if __name__ == '__main__':
    main()
