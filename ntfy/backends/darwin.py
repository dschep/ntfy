from subprocess import check_call


def notify(title, message, **kwargs):
    check_call([
        './ntfy/terminal-notifier.app/Contents/MacOS/terminal-notifier',
        '-message',
        message,
        '-title',
        title,
    ])
