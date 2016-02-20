
from errno import ENOENT
from unittest import TestCase, main
from sys import version_info

from mock import patch, mock_open

from ntfy.config import load_config, DEFAULT_CONFIG

py = version_info.major


mock_open_error = mock_open()
mock_open_error.side_effect = IOError(ENOENT, 'foobar')

class TestLoadConfig(TestCase):

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open_error)
    def test_default_config(self):
        config = load_config(DEFAULT_CONFIG)
        self.assertEqual(config, {'backends': ['default']})

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    def test_backwards_compat(self, mock_yamlload):
        mock_yamlload.return_value = {'backend': 'foobar'}
        config = load_config(DEFAULT_CONFIG)
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])
