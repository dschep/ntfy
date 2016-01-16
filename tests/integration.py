from os import devnull
from unittest import TestCase, main
from sys import version_info

from mock import patch, mock_open, MagicMock

from ntfy.cli import main as ntfy_main


py = version_info.major

class TestIntegration(TestCase):
    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
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
