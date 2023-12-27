from os import makedirs, path

from appdirs import user_config_dir

from telegram_send import configure, send

config_dir = user_config_dir('ntfy', 'dschep')
config_file = path.join(config_dir, 'telegram.ini')


def notify(title, message, parse_mode="text", retcode=None):
    """
    Sends message over Telegram using telegram-send, title is ignored.

    Optional parameters:
    * ``parse_mode`` - How telegram parses the text. Possible options are "text", "markdown" or "html". More details here: https://core.telegram.org/bots/api#formatting-options
    """
    if not path.exists(config_file):
        if not path.exists(config_dir):
            makedirs(config_dir)
        print("Follow the instructions to configure the Telegram backend.\n")
        configure(config_file)
    send(messages=[message], parse_mode=parse_mode, conf=config_file)
