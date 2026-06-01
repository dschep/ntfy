import logging

from . import notify
from .config import load_config


class NtfyHandler(logging.Handler):
    """A logging handler that sends notifications via ntfy.

    Example usage::

        import logging
        from ntfy.logging import NtfyHandler

        logger = logging.getLogger(__name__)
        logger.addHandler(NtfyHandler(title="My App"))
        logger.error("Something went wrong!")  # sends notification
    """

    def __init__(self, title="ntfy", level=logging.ERROR, config=None):
        super().__init__(level=level)
        self.title = title
        self._config = config

    def emit(self, record):
        try:
            message = self.format(record)
            config = self._config if self._config is not None else load_config()
            notify(message=message, title=self.title, config=config)
        except Exception:
            self.handleError(record)
