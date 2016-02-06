
from errno import ENOENT
from unittest import TestCase, main
from sys import version_info

from mock import patch, mock_open

from ntfy.config import load_config, truthyish

py = version_info.major


mock_open_error = mock_open()
mock_open_error.side_effect = IOError(ENOENT, 'foobar')

class TestLoadConfig(TestCase):

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open_error)
    def test_default_config(self):
        config = load_config('~/.ntfy.yml')
        self.assertEqual(config, {'backends': ['default']})

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.config.yaml.load')
    def test_backwards_compat(self, mock_yamlload):
        mock_yamlload.return_value = {'backend': 'foobar'}
        config = load_config('~/.ntfy.yml')
        self.assertIn('backends', config)
        self.assertEqual(config['backends'], ['foobar'])

class TestTruthyish(TestCase):
    def test_truthyish(self):
        self.assertTrue(truthyish('t'))
        self.assertTrue(truthyish('T'))
        self.assertTrue(truthyish('true'))
        self.assertTrue(truthyish('True'))
        self.assertTrue(truthyish('TRUE'))
        self.assertTrue(truthyish('1'))
        self.assertTrue(truthyish('Y'))
        self.assertTrue(truthyish('y'))
        self.assertTrue(truthyish('yes'))
        self.assertTrue(truthyish('YES'))

    def test_falseyish(self):
        self.assertFalse(truthyish('f'))
        self.assertFalse(truthyish('F'))
        self.assertFalse(truthyish('false'))
        self.assertFalse(truthyish('False'))
        self.assertFalse(truthyish('FALSE'))
        self.assertFalse(truthyish('0'))
        self.assertFalse(truthyish('N'))
        self.assertFalse(truthyish('n'))
        self.assertFalse(truthyish('no'))
        self.assertFalse(truthyish('NO'))

