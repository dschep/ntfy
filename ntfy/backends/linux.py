from os import environ, path

from ..data import icon


def notify(title, message, icon=icon.png, **kwargs):
    try:
        import dbus
    except ImportError:
        import sys
        import logging
        logger = logging.getLogger(__name__)
        if sys.platform.startswith('linux') and hasattr(sys, 'real_prefix'):
            logger.error(
                'Using ntfy for Linux desktop notifications with '
                'virtualenv requires creating your virtualenv with the '
                '--system-site-packages option')
            return
        elif not environ.get('DISPLAY'):
            logger.warn('DISPLAY not set')
            return
        else:
            raise
    bus = dbus.SessionBus()
    dbus_obj = bus.get_object('org.freedesktop.Notifications',
                              '/org/freedesktop/Notifications')
    dbus_iface = dbus.Interface(dbus_obj,
                                dbus_interface='org.freedesktop.Notifications')

    dbus_iface.Notify('ntfy', 0, path.abspath(icon), title, message, [], {},
                      -1)
