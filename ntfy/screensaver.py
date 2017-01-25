from shlex import split
from subprocess import check_output, check_call, CalledProcessError, PIPE

# some adapted from
# https://github.com/mtorromeo/xdg-utils/blob/master/scripts/xdg-screensaver.in#L540


def xscreensaver_detect():
    try:
        check_call(split('pgrep xscreensaver'), stdout=PIPE)
    except (CalledProcessError, OSError):
        return False
    else:
        return True


def xscreensaver_is_locked():
    return 'screen locked' in check_output(split('xscreensaver-command -time'))


def lightlocker_detect():
    try:
        check_call(split('pgrep light-locker'), stdout=PIPE)
    except (CalledProcessError, OSError):
        return False
    else:
        return True


def lightlocker_is_active():
    return 'The screensaver is active' in check_output(split(
        'light-locker-command -q'))


def gnomescreensaver_detect():
    try:
        import dbus
    except ImportError:
        return False
    bus = dbus.SessionBus()
    dbus_obj = bus.get_object('org.freedesktop.DBus',
                              '/org/freedesktop/DBus')
    dbus_iface = dbus.Interface(dbus_obj,
                                dbus_interface='org.freedesktop.DBus')
    try:
        dbus_iface.GetNameOwner('org.gnome.ScreenSaver')
    except dbus.DBusException as e:
        if e.get_dbus_name() == 'org.freedesktop.DBus.Error.NameHasNoOwner':
            return False
        else:
            raise e
    else:
        return True


def gnomescreensaver_is_locked():
    import dbus
    bus = dbus.SessionBus()
    dbus_obj = bus.get_object('org.gnome.ScreenSaver',
                              '/org/gnome/ScreenSaver')
    dbus_iface = dbus.Interface(dbus_obj,
                                dbus_interface='org.gnome.ScreenSaver')
    return bool(dbus_iface.GetActive())


def matescreensaver_detect():
    try:
        import dbus
    except ImportError:
        return False
    bus = dbus.SessionBus()
    dbus_obj = bus.get_object('org.freedesktop.DBus',
                              '/org/freedesktop/DBus')
    dbus_iface = dbus.Interface(dbus_obj,
                                dbus_interface='org.freedesktop.DBus')
    try:
        dbus_iface.GetNameOwner('org.mate.ScreenSaver')
    except dbus.DBusException as e:
        if e.get_dbus_name() == 'org.freedesktop.DBus.Error.NameHasNoOwner':
            return False
        else:
            raise e
    else:
        return True


def matescreensaver_is_locked():
    import dbus
    bus = dbus.SessionBus()
    dbus_obj = bus.get_object('org.mate.ScreenSaver',
                              '/org/mate/ScreenSaver')
    dbus_iface = dbus.Interface(dbus_obj,
                                dbus_interface='org.mate.ScreenSaver')
    return bool(dbus_iface.GetActive())


def is_locked():
    if xscreensaver_detect():
        return xscreensaver_is_locked()
    if lightlocker_detect():
        return lightlocker_is_active()
    if gnomescreensaver_detect():
        return gnomescreensaver_is_locked()
    if matescreensaver_detect():
        return matescreensaver_is_locked()
    return True
