import dbus
from os import path

DEFAULT_ICON = path.join(path.split(path.split(__file__)[0])[0], 'icon.png')

def notify(title, message, icon=DEFAULT_ICON, **kwargs):
    bus = dbus.SessionBus()
    dbus_obj = bus.get_object(
        'org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    dbus_iface = dbus.Interface(
        dbus_obj, dbus_interface='org.freedesktop.Notifications')

    dbus_iface.Notify('ntfy', 0, path.abspath(icon), title, message, [], {}, -1)
