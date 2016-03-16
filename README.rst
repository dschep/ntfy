About ``ntfy``
==============
|Version|_ |Downloads|_ |Docs|_ |Build|_ |Coverage|_

.. |Version| image:: https://img.shields.io/pypi/v/ntfy.svg
.. _Version: https://pypi.python.org/pypi/ntfy
.. |Downloads| image:: https://img.shields.io/pypi/dm/ntfy.svg
.. _Downloads: https://pypi.python.org/pypi/ntfy#downloads
.. |Docs| image:: https://img.shields.io/badge/docs-stable-brightgreen.svg
.. _Docs: http://ntfy.rtfd.org
.. |Build| image:: https://img.shields.io/travis/dschep/ntfy.svg
.. _Build: https://travis-ci.org/dschep/ntfy
.. |Coverage| image:: https://img.shields.io/coveralls/dschep/ntfy.svg
.. _Coverage: https://coveralls.io/github/dschep/ntfy

``ntfy`` is a utility for sending notifications, on demand and when commands
finish. It supports many delivery mechanisms, both local and remote.

Demo
----
.. image:: https://raw.githubusercontent.com/dschep/ntfy/master/docs/demo.gif

Quickstart
----------

::

    $ sudo pip install ntfy
    $ ntfy send test
    # send a notification when the command `sleep 10` finishes
    # this send the message '"sleep 10" succeeded in 0:10 minutes'
    $ ntfy done sleep 10
    $ ntfy -b pushover -o user_key t0k3n send 'Pushover test!'
    $ ntfy -t 'ntfy' send "Here's a custom notification title!"
    $ echo -e 'backends: ["pushover"]\npushover: {"user_token": "t0k3n"} > ~/.config/ntfy/ntfy.yml'
    $ ntfy send "Pushover via config file!"

Install
-------
It is suggested to globally (as indicated in quickstart above, without a
virtualenv) install ntfy. It *can* be installed in a virtualenv, with caveats.
Linux notifications requires ``--system-site-packages`` to be used and OS X
notifications don't work at all.

Extras
~~~~~~
``ntfy`` supports emoji shortcodes, support can be installed by installing
``ntfy[emoji]``. XMPP support requires SleekXMPP which can be installed by
installing ``ntfy[xmpp]``. ``ntfy done`` can watch existing processes by their
PID if you install ``ntfy[pid]``.

Shell integration
~~~~~~~~~~~~~~~~~
``ntfy`` has support for **automatically** sending notifications when long
running commands finish in bash and zsh. In bash it emulates zsh's preexec and
precmd functionality with `rcaloras/bash-preexec <https://github.com/rcaloras/bash-preexec>`_.
To enable it add the following to your ``.bashrc`` or ``.zshrc``:

::

    eval "$(ntfy shell-integration)"

By default it will only send notifications for commands lasting longer than 10
seconds. This can be configured with the ``AUTO_NTFY_DONE_TIMEOUT`` environment
variable.

To avoid unnecessary notifications when running interactive programs programs
listed in ``AUTO_NTFY_DONE_IGNORE`` don't generate notifications. for example:

::

    export AUTO_NTFY_DONE_IGNORE="vim screen meld"

Configuring ``ntfy``
--------------------

``ntfy`` is configured with a YAML file stored at ``~/.config/ntfy/ntfy.yml``

Backends
~~~~~~~~

The backends key specifies what backends to use by default. Each backend has
it's own configuration, stored in a key of it's own name. For example:

::

    ---
    backends:
        - pushover
        - linux
        - xmpp
    pushover:
        user_key: hunter2
    pushbullet:
        access_token: hunter2
    xmpp:
         jid: "user@gmail.com"
         password: "xxxx"
         mtype: "chat"
         recipient: "me@jit.si"

If you want mulitple configs for the same backend type, you can specify any
name and then specify the backend with a backend key. For example:

::

    ---
    pushover:
        user_key: hunter2
    cellphone:
        backend: pushover
        user_key: hunter2

See the backends bellow for available backends and options.

`Pushover <https://pushover.net>`_ - ``pushover``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required parameters:
    * ``user_key``

Optional parameters:
    * ``sound``
    * ``priority``
    * ``expire``
    * ``retry``
    * ``callback``
    * ``access_token`` - use your own application token
    * ``device`` - target a device, if omitted, notification is sent to all devices
    * ``url``
    * ``url_title``
    * ``html``

`Pushbullet <https://pushbullet.com>`_ - ``pushbullet``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required parameter:
    * ``access_token`` - Your Pushbullet access token, created at https://www.pushbullet.com/#settings/account

Optional parameters:
    * ``device_iden`` - a device identifier, if omited, notification is sent to all devices
    * ``email`` - send notification to pushbullte user with the specified email or send an email if they aren't a pushullet user

XMPP - ``xmpp``
~~~~~~~~~~~~~~~
Requires parameters:
    * ``jid``
    * ``password``
    * ``recipient``
Optional parameters
    * ``hostname`` (if not from jid)
    * ``port``
    * ``path_to_certs``
    * ``mtype`` ('chat' required for Google Hangouts)

To verify the SSL certificates offered by a server:
path_to_certs = "path/to/ca/cert"

Without dnspython library installed, you will need
to specify the server hostname if it doesn't match the jid.

For example, to use Google Talk you would need to use:
hostname = 'talk.google.com'

Specify port if other than 5222.
NOTE: Ignored without specified hostname

`Linux Desktop Notifications <https://developer.gnome.org/notification-spec/>`_ - ``linux``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Works via `dbus`, works with most DEs like Gnome, KDE, XFCE and with libnotify.

Windows Desktop Notifications - ``win32``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Uses ``pywin32``.

Mac OS X Notification Center - ``darwin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Requires ``ntfy`` to be installed globally (not in a virtualenv).

Other options
~~~~~~~~~~~~~

Title is configurable with the `title` key in the config. Example:

::

    ---
    title: Customized Title


Backends ToDo
~~~~~~~~~~~~~
-  `Prowl <http://www.prowlapp.com>`_
-  `Airgram <http://www.airgramapp.com>`_
-  `Pushjet <https://pushjet.io>`_
-  `Pushalot <https://pushalot.com>`_
-  `Boxcar <https://boxcar.io>`_
-  `Instapush <https://instapush.im>`_

Testing
-------

::

    python setup.py test

Contributors
------------
- `dschep <https://github.com/dschep>`_ - Maintainer & Lead Developer
- `danryder <https://github.com/danryder>`_ - XMPP Backend & emoji support
