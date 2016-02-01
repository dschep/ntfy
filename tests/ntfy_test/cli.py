from errno import ENOENT
from unittest import TestCase, main
from sys import version_info

from mock import patch, mock_open, MagicMock

from ntfy.cli import load_config, parser


py = version_info.major


mock_open_error = mock_open()
mock_open_error.side_effect = IOError(ENOENT, 'foobar')

class TestLoadConfig(TestCase):

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open_error)
    def test_default_config(self):
        config = load_config(parser.parse_args(['send', '']))
        self.assertEqual(config, {'backends': ['default']})

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open(read_data='{"backend": "foobar"}'))
    def test_backwards_compat(self,):
        config = load_config(parser.parse_args(['send', '']))
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])


if __name__ == '__main__':
    main()
