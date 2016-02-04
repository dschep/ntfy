from unittest import TestCase, main
from mock import patch

from ntfy.backends.pushover import notify


def PushoverTestCase(TestCase):
    @patch('requests.post')
    def test_success(self, mock_post):
        notify('title', 'message')
        mock_post.called_once_with()

if __name__ == '__main__':
    main()
