from unittest import TestCase, main

from mock import patch, MagicMock

from ntfy.cli import run_cmd, watch_pid
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


class TestWatchPID(TestCase):

    @patch('ntfy.cli.strftime')
    @patch('psutil.Process')
    def test_watch_pid(self, mock_process, mock_strftime):
        p = mock_process()
        p.pid = 0
        p.cmdline.return_value = ['cmd',]
        mock_strftime.return_value = 'now'
        args = MagicMock()
        args.pid = 0
        self.assertEqual('"Process[0]: cmd" was finished at now',
                         watch_pid(args))



if __name__ == '__main__':
    main()
