import syslog


def notify(title,
           message,
           prio='ALERT',
           facility='LOCAL5',
           fmt='[{title}] {message}',
           retcode=None):
    """
    Uses the ``syslog`` core Python module, which is not available on Windows
    platforms.

    Optional parameters:
        * ``prio`` - Syslog prority level.  Default is ``ALERT``.  Possible
          values are:

          * EMERG
          * ALERT
          * CRIT
          * ERR
          * WARNING
          * NOTICE
          * INFO
          * DEBUG

        * ``facility`` - Syslog facility.  Default is ``LOCAL5``.  Possible
          values are:

          * KERN
          * USER
          * MAIL
          * DAEMON
          * AUTH
          * LPR
          * NEWS
          * UUCP
          * CRON
          * SYSLOG
          * LOCAL0
          * LOCAL1
          * LOCAL2
          * LOCAL3
          * LOCAL4
          * LOCAL5
          * LOCAL6
          * LOCAL7

      * ``fmt`` - Format of the message to be sent to the system logger.  The
        title and the message are specified using the following placeholders:

        * ``{title}``
        * ``{message}``

        Default is ``[{title}] {message}``.
    """

    prio_map = {
        'EMERG': syslog.LOG_EMERG,
        'ALERT': syslog.LOG_ALERT,
        'CRIT': syslog.LOG_CRIT,
        'ERR': syslog.LOG_ERR,
        'WARNING': syslog.LOG_WARNING,
        'NOTICE': syslog.LOG_NOTICE,
        'INFO': syslog.LOG_INFO,
        'DEBUG': syslog.LOG_DEBUG,
    }

    facility_map = {
        'KERN': syslog.LOG_KERN,
        'USER': syslog.LOG_USER,
        'MAIL': syslog.LOG_MAIL,
        'DAEMON': syslog.LOG_DAEMON,
        'AUTH': syslog.LOG_AUTH,
        'LPR': syslog.LOG_LPR,
        'NEWS': syslog.LOG_NEWS,
        'UUCP': syslog.LOG_UUCP,
        'CRON': syslog.LOG_CRON,
        'SYSLOG': syslog.LOG_SYSLOG,
        'LOCAL0': syslog.LOG_LOCAL0,
        'LOCAL1': syslog.LOG_LOCAL1,
        'LOCAL2': syslog.LOG_LOCAL2,
        'LOCAL3': syslog.LOG_LOCAL3,
        'LOCAL4': syslog.LOG_LOCAL4,
        'LOCAL5': syslog.LOG_LOCAL5,
        'LOCAL6': syslog.LOG_LOCAL6,
        'LOCAL7': syslog.LOG_LOCAL7,
    }

    if prio not in prio_map:
        raise ValueError('invalid syslog priority')
    elif facility not in facility_map:
        raise ValueError('invalid syslog facility')

    msg = fmt.format(title=title, message=message)
    for line in msg.splitlines():
        syslog.syslog(facility_map[facility] | prio_map[prio], line)
