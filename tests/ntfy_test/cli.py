from errno import ENOENT
from unittest import TestCase, main
from sys import version_info

from mock import patch, mock_open, MagicMock

from ntfy.cli import load_config, parser, truthyish, run_cmd
from ntfy.cli import main as ntfy_main


py = version_info.major


mock_open_error = mock_open()
mock_open_error.side_effect = IOError(ENOENT, 'foobar')


class TestLoadConfig(TestCase):

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open',
           mock_open_error)
    def test_default_config(self):
        config = load_config(parser.parse_args(['send', '']))
        self.assertEqual(config, {'backends': ['default']})

    @patch(('__builtin__' if py == 2 else 'builtins') + '.open', mock_open())
    @patch('ntfy.cli.yaml.load')
    def test_backwards_compat(self, mock_yamlload):
        mock_yamlload.return_value = {'backend': 'foobar'}
        config = load_config(parser.parse_args(['send', '']))
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


class TestRunCmd(TestCase):
    @patch('subprocess.call')
    def test_runcmd(self, mock_call):
        mock_call.return_value = 0
        args = MagicMock()
        args.command = ['true']
        self.assertEqual('"true" succeeded in 0:00 minutes',
                         run_cmd(args))


class TestMain(TestCase):
    @patch('ntfy.backends.default.notify')
    def test_args(self, mock_notify):
        ntfy_main(['-o', 'foo', 'bar', '-b', 'default', '-t', 'TITLE',
                   'send', 'test'])
        mock_notify.assert_called_once_with(message='test', title='TITLE',
                                            foo='bar')


if __name__ == '__main__':
    main()
