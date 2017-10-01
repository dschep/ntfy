from errno import ENOENT
from os import environ
from sys import version_info
from unittest import TestCase, main, skipIf

from mock import mock_open, patch
from ntfy.config import DEFAULT_CONFIG, load_config

py = version_info.major
py_ = version_info.major, version_info.minor

mock_open_dne_error = mock_open()
mock_open_dne_error.side_effect = IOError(ENOENT, 'foobar')
mock_open_other_error = mock_open()
mock_open_other_error.side_effect = IOError()

builtin_module = '__builtin__' if py == 2 else 'builtins'


class TestLoadConfig(TestCase):
    @patch(builtin_module + '.open', mock_open_dne_error)
    def test_default_config(self):
        config = load_config(DEFAULT_CONFIG)
        self.assertEqual(config, {})

    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    def test_backwards_compat(self, mock_yamlload):
        mock_yamlload.return_value = {'backend': 'foobar'}
        config = load_config(DEFAULT_CONFIG)
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])

    @skipIf(
        environ.get('CI') and py_ in [(3, 3), (3, 4)],
        'Python 3.3 and 3.4 fail in TravisCI, but 3.4 works on Ubuntu 14.04')
    @patch(builtin_module + '.open', mock_open())
    @patch('ntfy.config.safe_load')
    def test_parse_error(self, mock_yamlload):
        mock_yamlload.side_effect = ValueError
        self.assertRaises(SystemExit, load_config)

    @patch(builtin_module + '.open', mock_open_other_error)
    def test_open_error(self):
        self.assertRaises(SystemExit, load_config)
