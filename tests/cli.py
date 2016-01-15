from os import devnull
from unittest import TestCase, main

from mock import patch, mock_open

from ntfy.cli import load_config, parser


class TestLoadConfig(TestCase):

    @patch('ntfy.cli.stderr')
    def test_default_config(self, *mocks):
        config = load_config(parser.parse_args(['-c', devnull, 'send', '']))
        self.assertEqual(config, {'backends': ['default']})

    @patch('__main__.open', mock_open())
    @patch('ntfy.cli.json.load', lambda x: {'backend': 'foobar'})
    def test_backwards_compat(self, *mocks):
        config = load_config(parser.parse_args(['-c', devnull, 'send', '']))
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])


if __name__ == '__main__':
    main()
