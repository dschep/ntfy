from os import environ, ttyname
from subprocess import check_output, Popen, PIPE
from sys import platform, stdout


def get_tty():
    window_id = int(check_output(['xprop', '-root', '\t$0',
                                  '_NET_ACTIVE_WINDOW']).split()[1], 16)
    return int(environ['WINDOWID']) == window_id


def linux_window_is_focused():
    window_id = int(check_output(['xprop', '-root', '\t$0',
                                  '_NET_ACTIVE_WINDOW']).split()[1], 16)
    return int(environ['WINDOWID']) == window_id


def osascript_tell(app, script):
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate(
        'tell application "{}"\n{}\nend tell'.format(app, script))
    return stdout.rstrip('\n')


def darwin_iterm2_shell_is_focused():
    focused_tty = osascript_tell(
        'iTerm',
        'tty of current session of current terminal',
    )
    return focused_tty == ttyname(stdout.fileno())


def darwin_terminal_shell_is_focused():
    focused_tty = osascript_tell(
        'Terminal',
        'tty of (first tab of (first window whose frontmost is true) '
        'whose selected is true)',
    )
    return focused_tty == ttyname(stdout.fileno())


def darwin_app_shell_is_focused():
    current_appid = {
        'iTerm.app': 'iTerm',
        'Apple_Terminal': 'Terminal',
    }.get(environ.get('TERM_PROGRAM'))
    focused_appid = osascript_tell(
        'System Events',
        'name of first application process whose frontmost is true',
    )
    if current_appid == focused_appid:
        return {
            'Terminal': darwin_terminal_shell_is_focused,
            'iTerm': darwin_iterm2_shell_is_focused,
        }[current_appid]()


def is_focused():
    if platform.startswith('linux') and environ.get('DISPLAY'):
        return linux_window_is_focused()
    elif platform == 'darwin':
        return darwin_app_shell_is_focused()
    else:
        return False
