import shlex
from os import environ, ttyname
from subprocess import PIPE, Popen, check_output, CalledProcessError
from sys import platform, stdout

def tmux_is_focused():
    cmd = shlex.split('tmux list-panes -F "#{pane_id}:#{pane_active}:#{window_active}:#{session_attached}"')
    pane = environ.get('TMUX_PANE')
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    p.wait()
    if p.poll() != 0:
        return False
    panes = p.stdout.read().decode()
    return True if panes.find(pane + ':1:1:1') != -1 else False


def linux_window_is_focused():
    xprop_cmd = shlex.split('xprop -root _NET_ACTIVE_WINDOW')
    try:
        xprop_window_id = int(check_output(xprop_cmd, stdout=PIPE, stderr=PIPE).split()[-1], 16)
    except CalledProcessError:
        return False
    except ValueError:
        return False
    except OSError as e:
        if 'No such file' in e.strerror:
            return False
        else:
            raise
    env_window_id = int(environ.get('WINDOWID', '0'))
    return env_window_id == xprop_window_id

def get_tty():
    if environ.get('TMUX'):
        # tmux list-clients -F '#{client_tty}'
        tprop_cmd = shlex.split("tmux list-clients -F '#{client_tty}'")
        return check_output(tprop_cmd).decode().strip()
    else:
        return ttyname(stdout.fileno())

def osascript_tell(app, script):
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate(
        ('tell application "{}"\n{}\nend tell'.format(app, script)
         .encode('utf-8')))
    return stdout.decode('utf-8').rstrip('\n')


def darwin_iterm2_shell_is_focused():
    focused_tty = osascript_tell(
        'iTerm',
        'tty of current session of current window',
    )
    return focused_tty == get_tty()


def darwin_terminal_shell_is_focused():
    focused_tty = osascript_tell(
        'Terminal',
        'tty of (first tab of (first window whose frontmost is true) '
        'whose selected is true)',
    )
    return focused_tty == get_tty()


def darwin_app_shell_is_focused():
    current_appid = {
        'iTerm.app': 'iTerm2',
        'Apple_Terminal': 'Terminal',
    }.get(environ.get('TERM_PROGRAM'))
    focused_appid = osascript_tell(
        'System Events',
        'name of first application process whose frontmost is true',
    )
    if current_appid == focused_appid:
        return {
            'Terminal': darwin_terminal_shell_is_focused,
            'iTerm2': darwin_iterm2_shell_is_focused,
        }[current_appid]()


def is_focused():
    retval = None

    if platform.startswith('linux') and environ.get('DISPLAY'):
        retval = linux_window_is_focused()
    elif platform == 'darwin':
        retval = darwin_app_shell_is_focused()

    if environ.get('TMUX'):
        return tmux_is_focused() & (retval if retval is not None else True)
    else:
        return retval
