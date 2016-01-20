About ``ntfy``
==============
|Version|_ |Downloads|_ |Build|_ |Coverage|_

.. |Version| image:: https://img.shields.io/pypi/v/ntfy.svg
.. _Version: https://pypi.python.org/pypi/ntfy
.. |Downloads| image:: https://img.shields.io/pypi/dm/ntfy.svg
.. _Downloads: https://pypi.python.org/pypi/ntfy#downloads
.. |Build| image:: https://img.shields.io/travis/dschep/ntfy.svg
.. _Build: https://travis-ci.org/dschep/ntfy
.. |Coverage| image:: https://img.shields.io/coveralls/dschep/ntfy.svg
.. _Coverage: https://coveralls.io/github/dschep/ntfy

``ntfy`` is a command line utility (and to a degree, python library) for
sending push notifications. It also can send a notification when a
program finishes.

Unlike many existing utilities for Pushover or Pushbullet, it supports
multiple backends.

Demo
----
.. image:: https://raw.githubusercontent.com/dschep/ntfy/master/demo.gif

Install
-------

::

    sudo pip install ntfy

Note: It is suggested to globally (as indicated above, without a
virtualenv) install ntfy. It *can* be installed in a virtualenv, with caveats.
Linux notifications requires ``--system-site-packages`` to be used and OS X
notifications don't work at all.

Usage
-----

::


    # send a notification
    ntfy send "Here's a notification!"

    # send a notification with custom title (default is $USER@$HOST)
    ntfy -t 'ntfy' send "Here's a notification with a custom title!"

    # send a notification when the command `sleep 10` finishes
    # this send the message '"sleep 10" succeeded in 0.2 minutes'
    ntfy done sleep 10

Backends
========

Supported
---------
-  `Pushover <https://pushover.net>`_
-  `Pushbullet <https://pushbullet.com>`_
-  XMPP
-  Linux Desktop Notifications
-  Windows Desktop Notifications
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
``~/.ntfy.json``. It requires at minimum 1 keys: backends & a config for any
backend that requires one.

For full docs consult the `wiki <https://github.com/dschep/ntfy/wiki>`_

Example Config
~~~~~~~~~~~~~~

::

    {
        "backends": ["pushbullet"],
        "pushbullet": {"access_token": "<redacted>"}
    }

Testing
~~~~~~~

::

    python setup.py test

Contributors
~~~~~~~~~~~~
- `dschep <https://github.com/dschep>`_ - Maintainer & Lead Developer
- `danryder <https://github.com/danryder>`_ - XMPP Backend & emoji support
