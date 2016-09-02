from unittest import TestCase
from mock import patch, call
import syslog

from ntfy.backends.systemlog import notify


class TestSystemlog(TestCase):
    @patch('syslog.syslog')
    def test_basic(self, mock_post):
        notify('title', 'message')
        mock_post.assert_called_once_with(
            syslog.LOG_LOCAL5|syslog.LOG_ALERT,
            '[title] message')

    @patch('syslog.syslog')
    def test_facility(self, mock_post):
        notify('title', 'message', facility='MAIL')
        mock_post.assert_called_once_with(
            syslog.LOG_MAIL|syslog.LOG_ALERT,
            '[title] message')

    @patch('syslog.syslog')
    def test_prio(self, mock_post):
        notify('title', 'message', prio='DEBUG')
        mock_post.assert_called_once_with(
            syslog.LOG_LOCAL5|syslog.LOG_DEBUG,
            '[title] message')

    @patch('syslog.syslog')
    def test_fmt(self, mock_post):
        notify('title', 'message', fmt='Title: {title} Message: {message}')
        mock_post.assert_called_once_with(
            syslog.LOG_LOCAL5|syslog.LOG_ALERT,
            'Title: title Message: message')

    @patch('syslog.syslog')
    def test_multiple_lines(self, mock_post):
        notify('title', 'message\non multiple\nlines')
        calls = [ call(syslog.LOG_LOCAL5|syslog.LOG_ALERT,
                                '[title] message'),
                  call(syslog.LOG_LOCAL5|syslog.LOG_ALERT,
                                'on multiple'),
                  call(syslog.LOG_LOCAL5|syslog.LOG_ALERT,
                                'lines'),
                ]
        mock_post.assert_has_calls(calls)

    @patch('syslog.syslog')
    def test_invalid_prio(self, mock_post):
        self.assertRaises(ValueError,
                          notify,
                          'title',
                          'message',
                          prio='INVALID_PRIO')

    @patch('syslog.syslog')
    def test_invalid_facility(self, mock_post):
        self.assertRaises(ValueError,
                          notify,
                          'title',
                          'message',
                          facility='INVALID_FACILITY')
