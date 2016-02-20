def notify(title, message, **kwargs):
    """
    adapted from https://gist.github.com/baliw/4020619
    """
    try:
        import Foundation
        import objc
    except ImportError:
        import sys
        import logging

        logger = logging.getLogger(__name__)
        if sys.platform.startswith('darwin') and hasattr(sys, 'real_prefix'):
            logger.error(
                "Using ntfy with the MacOS Notification Center doesn't "
                "work within a virtualenv")
            sys.exit(1)
        else:
            raise

    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    if message is not None:
        notification.setInformativeText_(message)
    notification.setDeliveryDate_(Foundation.NSDate.date())

    NSUserNotificationCenter.defaultUserNotificationCenter()\
        .scheduleNotification_(notification)
