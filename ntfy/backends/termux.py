from __future__ import print_function

from subprocess import check_call


def notify(title, message, retcode=None):
    """
    Termux:API backend.
    """

    check_call(['termux-notification', '--content', message, '--title', title])
