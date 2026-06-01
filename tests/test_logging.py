import logging
from unittest import TestCase
from unittest.mock import patch

from ntfy.logging import NtfyHandler


class TestNtfyHandler(TestCase):
    def test_default_level(self):
        handler = NtfyHandler(title="Test")
        self.assertEqual(handler.level, logging.ERROR)

    def test_custom_level(self):
        handler = NtfyHandler(title="Test", level=logging.WARNING)
        self.assertEqual(handler.level, logging.WARNING)

    def test_default_title(self):
        handler = NtfyHandler()
        self.assertEqual(handler.title, "ntfy")

    @patch("ntfy.logging.notify")
    def test_emit(self, mock_notify):
        handler = NtfyHandler(title="My App")
        log_record = logging.LogRecord(
            "test", logging.ERROR, "/path/file.py", 42,
            "Something broke!", None, None
        )
        handler.emit(log_record)

        mock_notify.assert_called_once()
        _, kwargs = mock_notify.call_args
        self.assertEqual(kwargs["title"], "My App")
        self.assertIn("Something broke!", kwargs["message"])

    @patch("ntfy.logging.notify")
    def test_emit_with_config(self, mock_notify):
        config = {"backends": ["default"]}
        handler = NtfyHandler(title="Test", config=config)
        log_record = logging.LogRecord(
            "test", logging.WARNING, "/path/file.py", 42,
            "Warning!", None, None
        )
        handler.emit(log_record)

        mock_notify.assert_called_once()
        _, kwargs = mock_notify.call_args
        self.assertEqual(kwargs["config"], config)
        self.assertEqual(kwargs["title"], "Test")
        self.assertIn("Warning!", kwargs["message"])

    @patch("ntfy.logging.notify")
    def test_emit_formatted(self, mock_notify):
        handler = NtfyHandler(title="App")
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        log_record = logging.LogRecord(
            "test", logging.ERROR, "/path/file.py", 42,
            "Something broke!", None, None
        )
        handler.emit(log_record)

        mock_notify.assert_called_once()
        _, kwargs = mock_notify.call_args
        self.assertEqual(kwargs["title"], "App")
        self.assertEqual(kwargs["message"], "ERROR: Something broke!")
