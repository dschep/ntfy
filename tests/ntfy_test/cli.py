from unittest import TestCase, main

from mock import patch, MagicMock

from ntfy.cli import run_cmd, auto_done
from ntfy.cli import main as ntfy_main


class TestRunCmd(TestCase):
    @patch('subprocess.call')
    def test_runcmd(self, mock_call):
        mock_call.return_value = 0
        args = MagicMock()
        args.longer_than = 0
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


class ShellIntegrationTestCase(TestCase):
    def test_shellintegration_printout(self):
        # not mocking print to check calls because test runner uses print...
        args = MagicMock()
        auto_done(args)


if __name__ == '__main__':
    main()
