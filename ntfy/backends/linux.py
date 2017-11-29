from os import environ, path

from ..data import icon


def notify(title,
           message,
           icon=icon.png,
           urgency=None,
           transient=None,
           retcode=0):
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
    dbus_iface = dbus.Interface(
        dbus_obj, dbus_interface='org.freedesktop.Notifications')

    hints = {}

    # Override the retcode if the urgency
    if urgency == 'low':
        hints = {'urgency': dbus.Byte(0)}
    elif urgency == 'normal':
        hints = {'urgency': dbus.Byte(1)}
    elif urgency == 'critical':
        hints = {'urgency': dbus.Byte(2)}
    # Fallback to the return code to determine the urgency flag.
    elif retcode:
        hints = {'urgency': dbus.Byte(2)}

    if str(transient).lower() == 'true':
        hints.update({'transient': dbus.Byte(1)})
    elif str(transient).lower() == 'false':
        hints.update({'transient': dbus.Byte(0)})
    elif transient is not None:
        logger.warn(
            'Unexpected value for the "transient" option. Expected values (true, false).'
        )

    message = message.replace('&', '&amp;')
    dbus_iface.Notify('ntfy', 0, path.abspath(icon), title, message, [], hints,
                      -1)
