import Foundation
import objc
import AppKit

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

def notify(subject, config, message=None, device=None):
    """
    adapted from https://gist.github.com/baliw/4020619
    """
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(subject)
    if message is not None:
        notification.setInformativeText_(message)
    notification.setDeliveryDate_(Foundation.NSDate.date())

    NSUserNotificationCenter.defaultUserNotificationCenter()\
        .scheduleNotification_(notification)
