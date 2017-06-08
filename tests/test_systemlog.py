from unittest import TestCase, skipIf

from mock import call, patch

try:
    import syslog
    syslog_supported = True
except ImportError:
    syslog_supported = False

if syslog_supported:
    from ntfy.backends.systemlog import notify


class TestSystemlog(TestCase):
    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_basic(self, mock_post):
        notify('title', 'message')
        mock_post.assert_called_once_with(syslog.LOG_LOCAL5 | syslog.LOG_ALERT,
                                          '[title] message')

    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_facility(self, mock_post):
        notify('title', 'message', facility='MAIL')
        mock_post.assert_called_once_with(syslog.LOG_MAIL | syslog.LOG_ALERT,
                                          '[title] message')

    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_prio(self, mock_post):
        notify('title', 'message', prio='DEBUG')
        mock_post.assert_called_once_with(syslog.LOG_LOCAL5 | syslog.LOG_DEBUG,
                                          '[title] message')

    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_fmt(self, mock_post):
        notify('title', 'message', fmt='Title: {title} Message: {message}')
        mock_post.assert_called_once_with(syslog.LOG_LOCAL5 | syslog.LOG_ALERT,
                                          'Title: title Message: message')

    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_multiple_lines(self, mock_post):
        notify('title', 'message\non multiple\nlines')
        calls = [
            call(syslog.LOG_LOCAL5 | syslog.LOG_ALERT, '[title] message'),
            call(syslog.LOG_LOCAL5 | syslog.LOG_ALERT, 'on multiple'),
            call(syslog.LOG_LOCAL5 | syslog.LOG_ALERT, 'lines'),
        ]
        mock_post.assert_has_calls(calls)

    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_invalid_prio(self, mock_post):
        self.assertRaises(
            ValueError, notify, 'title', 'message', prio='INVALID_PRIO')

    @skipIf(not syslog_supported, 'Syslog not supported')
    @patch('syslog.syslog')
    def test_invalid_facility(self, mock_post):
        self.assertRaises(
            ValueError,
            notify,
            'title',
            'message',
            facility='INVALID_FACILITY')
