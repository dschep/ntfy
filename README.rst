About ``ntfy``
==============

``ntfy`` is a command line utility (and to a degree, python library) for
sending push notifications. It also can send a notification when a
program finishes.

Unlike many existing utilities for Pushover or Pushbullet, it supports
multiple backends.

Demo
----
`Click here for full demo <https://cdn.rawgit.com/dschep/ntfy/master/demo/ntfy-demo.mp4>`_

.. image:: https://raw.githubusercontent.com/dschep/ntfy/master/demo/ntfy-demo.gif

Install
-------

::

    sudo pip install ntfy

Note: It is suggested to globally (as indicated above, without a
virtualenv) install ntfy. It *can* be installed in a virtualenv, but Mac
OS X & Windows notifications won't work.

Usage
-----

::


    # send a notification
    ntfy send "Here's a notification!"

    # send a notification with custom title (default is $USER@$HOST)
    ntfy send -t 'ntfy' "Here's a notification with a custom title!"

    # send a notification when the command `sleep 10` finishes
    # this send the message '"sleep 10" succeeded in 0.2 minutes'
    ntfy done sleep 10

Backends
========

Supported
---------
-  `Pushover <https://pushover.net>`_
-  `Pushbullet <https://pushbullet.com>`_
-  Linux Desktop Notifications (notify-send)
-  Windows Desktop Notifications (requires `PyWin32 <http://sourceforge.net/projects/pywin32/>`_)
-  Mac OS X Notification Center

ToDo
----
-  `Prowl <http://www.prowlapp.com>`_
-  `Airgram <http://www.airgramapp.com>`_
-  `Pushjet <https://pushjet.io>`_
-  `Pushalot <https://pushalot.com>`_
-  `Boxcar <https://boxcar.io>`_
-  `Instapush <https://instapush.im>`_

Config
------

``ntfy`` is configured via a json config file stored at
``~/.ntfy.json``. It requires at minimum 2 keys: backend & a config for
that backend.

For full docs consult the `wiki <https://github.com/dschep/ntfy/wiki>`_

Example Config
~~~~~~~~~~~~~~

::

    {
        "backend": "pushbullet",
        {"pushbullet": {"access_token": "<redacted>"}}
    }
