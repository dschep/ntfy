from gotify import Gotify

def notify(title, message, base_url, app_token, retcode=None):
    """Sends message through gotify"""
    gotify = Gotify(
        base_url=base_url,
        app_token=app_token,
    )

    gotify.create_message(
        message,
        title=title,
        priority=0,
    )
