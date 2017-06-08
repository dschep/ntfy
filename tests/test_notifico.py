from unittest import TestCase, main

from requests import HTTPError, Response

from mock import patch
from ntfy.backends.notifico import notify


class TestNotifico(TestCase):
    def setUp(self):
        self.webhook = 'https://n.tkte.ch/h/1234/testing_webhook'

    @patch('requests.get')
    def test_basic(self, mock_get):
        resp = Response()
        resp.status_code = 200
        mock_get.return_value = resp
        notify('title', 'message', webhook=self.webhook)
        mock_get.assert_called_once_with(
            self.webhook, params={'payload': 'title\nmessage'})

    @patch('requests.get')
    def test_none_webhook(self, mock_get):
        notify('title', 'message', webhook=None)
        mock_get.assert_not_called()

    @patch('requests.get')
    def test_exception(self, mock_get):
        resp = Response()
        resp.status_code = 400
        mock_get.return_value = resp
        with self.assertRaises(HTTPError):
            notify('title', 'message', webhook=self.webhook)
        mock_get.assert_called_once_with(
            self.webhook, params={'payload': 'title\nmessage'})


if __name__ == '__main__':
    main()
