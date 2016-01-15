from os import devnull
from unittest import TestCase, main

from mock import patch

from ntfy.cli import load_config, parser


class TestLoadConfig(TestCase):

    @patch('ntfy.cli.stderr')
    @patch('ntfy.cli.open', side_effect=IOError())
    def test_default_config(self, *mocks):
        config = load_config(parser.parse_args(['-c', devnull, 'send', '']))
        self.assertEqual(config, {'backends': ['default']})

    @patch('ntfy.cli.open')
    @patch('ntfy.cli.json.load', lambda x: {'backend': 'foobar'})
    def test_backwards_compat(self, *mocks):
        config = load_config(parser.parse_args(['-c', devnull, 'send', '']))
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])


if __name__ == '__main__':
    main()
