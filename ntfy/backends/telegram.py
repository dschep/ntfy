from os import makedirs, path
from appdirs import user_config_dir
from telegram_send import configure, send
import asyncio

config_dir = user_config_dir('ntfy', 'dschep')
config_file = path.join(config_dir, 'telegram.ini')

def notify(title, message, retcode=None):
    """Sends message over Telegram using telegram-send, title is ignored."""
    if not path.exists(config_file):
        if not path.exists(config_dir):
            makedirs(config_dir)
        print("Follow the instructions to configure the Telegram backend.\n")
        asyncio.run(configure(config_file))
    asyncio.run(send(messages=[message], conf=config_file))