from time import time
from unittest import TestCase, main

from mock import patch, MagicMock

from ntfy.cli import run_cmd, auto_done
from ntfy.cli import main as ntfy_main


class TestRunCmd(TestCase):
    @patch('ntfy.cli.call')
    def test_default(self, mock_call):
        mock_call.return_value = 0
        args = MagicMock()
        args.longer_than = -1
        args.command = ['true']
        args.pid = None
        args.unfocused_only = False
        self.assertEqual(('"true" succeeded in 0:00 minutes', 0), run_cmd(args))

    @patch('ntfy.cli.call')
    def test_emoji(self, mock_call):
        mock_call.return_value = 0
        args = MagicMock()
        args.longer_than = -1
        args.command = ['true']
        args.pid = None
        args.no_emoji = False
        args.unfocused_only = False
        self.assertEqual((':white_check_mark: "true" succeeded in 0:00 minutes', 0),
                         run_cmd(args))

    def tests_usage(self):
        args = MagicMock()
        args.pid = False
        args.formatter = False
        args.command = []
        self.assertRaises(SystemExit, run_cmd, args)

    @patch('ntfy.cli.call')
    def test_longerthan(self, mock_call):
        mock_call.return_value = 0
        args = MagicMock()
        args.longer_than = 1
        args.command = ['true']
        args.pid = None
        args.unfocused_only = False
        self.assertEqual((None,None), run_cmd(args))


class TestMain(TestCase):
    @patch('ntfy.backends.default.notify')
    def test_args(self, mock_notify):
        ntfy_main(['-o', 'foo', 'bar', '-b', 'default', '-t', 'TITLE', 'send',
                   'test'])
        mock_notify.assert_called_once_with(message='test',
                                            title='TITLE',
                                            foo='bar',
                                            retcode=0)


class ShellIntegrationTestCase(TestCase):
    def test_shellintegration_printout(self):
        # not mocking print to check calls because test runner uses print...
        args = MagicMock()
        auto_done(args)


class TestWatchPID(TestCase):
    @patch('psutil.Process')
    def test_watch_pid(self, mock_process):
        mock_process.return_value.pid = 1
        mock_process.return_value.create_time.return_value = time()
        mock_process.return_value.cmdline.return_value = ['cmd']
        args = MagicMock()
        args.pid = 1
        args.unfocused_only = False
        self.assertEqual('PID[1]: "cmd" finished in 0:00 minutes',
                         run_cmd(args)[0])

    def test_watch_bad_pid(self):
        args = MagicMock()
        args.pid = 100000
        self.assertRaises(SystemExit, run_cmd, args)


if __name__ == '__main__':
    main()
