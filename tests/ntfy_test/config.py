
from errno import ENOENT
from unittest import TestCase, main
from sys import version_info

from mock import patch, mock_open

from ntfy.config import load_config, DEFAULT_CONFIG

py = version_info.major


mock_open_dne_error = mock_open()
mock_open_dne_error.side_effect = IOError(ENOENT, 'foobar')
mock_open_other_error = mock_open()
mock_open_other_error.side_effect = IOError()

class TestLoadConfig(TestCase):

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open_dne_error)
    def test_default_config(self):
        config = load_config(DEFAULT_CONFIG)
        self.assertEqual(config, {})

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    def test_backwards_compat(self, mock_yamlload):
        mock_yamlload.return_value = {'backend': 'foobar'}
        config = load_config(DEFAULT_CONFIG)
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    def test_parse_error(self, mock_yamlload):
        mock_yamlload.side_effect = ValueError
        self.assertRaises(SystemExit, load_config)

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open_other_error)
    def test_open_error(self):
        self.assertRaises(SystemExit, load_config)
