import json
from unittest import TestCase
from mock import patch
from ntfy.backends.mqtt import notify

class TestMQTT(TestCase):
    @patch('paho.mqtt.publish.single')
    def test_basic(self, mock_publish):
        notify('title', 'message', hostname='localhost', topic='test')
        mock_publish.assert_called_once_with(
            topic='test',
            payload=json.dumps({'title': 'title', 'message': 'message', 'retcode': None}),
            hostname='localhost',
            port=1883,
            qos=1,
            auth=None
        )

    @patch('paho.mqtt.publish.single')
    def test_full(self, mock_publish):
        notify(
            'title',
            'message',
            hostname='example.com',
            topic='ntfy',
            port=8883,
            qos=2,
            username='user',
            password='pass',
            retcode=0
        )
        mock_publish.assert_called_once_with(
            topic='ntfy',
            payload=json.dumps({'title': 'title', 'message': 'message', 'retcode': 0}),
            hostname='example.com',
            port=8883,
            qos=2,
            auth={'username': 'user', 'password': 'pass'}
        )

    @patch('paho.mqtt.publish.single')
    @patch('logging.error')
    def test_missing_config(self, mock_log, mock_publish):
        notify('title', 'message', hostname='localhost')
        mock_publish.assert_not_called()
        mock_log.assert_called_once()

        mock_log.reset_mock()
        notify('title', 'message', topic='test')
        mock_publish.assert_not_called()
        mock_log.assert_called_once()

    @patch('paho.mqtt.publish.single')
    @patch('logging.error')
    def test_publish_error(self, mock_log, mock_publish):
        mock_publish.side_effect = Exception('MQTT Error')
        notify('title', 'message', hostname='localhost', topic='test')
        mock_log.assert_called_once()
