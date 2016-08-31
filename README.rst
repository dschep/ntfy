About ``ntfy``
==============
|Version|_ |Docs|_ |Build|_ |WinBuild|_ |Coverage|_ |Requires|_

.. |Version| image:: https://img.shields.io/pypi/v/ntfy.svg
.. _Version: https://pypi.python.org/pypi/ntfy
.. |Docs| image:: http://readthedocs.org/projects/ntfy/badge/?version=latest
.. _Docs: http://ntfy.readthedocs.org/en/stable/?badge=latest
.. |Build| image:: https://travis-ci.org/dschep/ntfy.svg?branch=master
.. _Build: https://travis-ci.org/dschep/ntfy
.. |WinBuild| image:: https://ci.appveyor.com/api/projects/status/fw6oycy7px0k23gi/branch/master?svg=true
.. _WinBuild: https://ci.appveyor.com/project/dschep/ntfy
.. |Coverage| image:: https://coveralls.io/repos/github/dschep/ntfy/badge.svg?branch=master
.. _Coverage: https://coveralls.io/github/dschep/ntfy?brach=master
.. |Requires| image:: https://requires.io/github/dschep/ntfy/requirements.svg?branch=master
.. _Requires: https://requires.io/github/dschep/ntfy/requirements/?branch=master


``ntfy`` brings notification to your shell. It can automatically provide
desktop notifications when long running commands finish or it can send
push notifications to your phone when a specific command finishes.
Confused? This video demonstrates some of this functionality:

.. image:: https://raw.githubusercontent.com/dschep/ntfy/master/docs/demo.gif

Quickstart
----------

.. code:: shell

    $ sudo pip install ntfy
    $ ntfy send test
    # send a notification when the command `sleep 10` finishes
    # this sends the message '"sleep 10" succeeded in 0:10 minutes'
    $ ntfy done sleep 10
    $ ntfy -b pushover -o user_key t0k3n send 'Pushover test!'
    $ ntfy -t 'ntfy' send "Here's a custom notification title!"
    $ echo -e 'backends: ["pushover"]\npushover: {"user_key": "t0k3n"}' > ~/.ntfy.yml
    $ ntfy send "Pushover via config file!"
    $ ntfy done --pid 6379  # PID extra
    $ ntfy send ":tada: ntfy supports emoji! :100:"  # emoji extra
    # Enable shell integration
    $ echo 'eval "$(ntfy shell-integration)"' >> ~/.bashrc

Install
-------
The install technique in the quickstart is the suggested method of installation.
It can be installed in a virtualenv, but with some caveats: Linux notifications
require ``--system-site-packages`` for the virtualenv and OS X notifications
don't work at all.

Shell integration
~~~~~~~~~~~~~~~~~
``ntfy`` has support for **automatically** sending notifications when long
running commands finish in bash and zsh. In bash it emulates zsh's preexec and
precmd functionality with `rcaloras/bash-preexec <https://github.com/rcaloras/bash-preexec>`_.
To enable it add the following to your ``.bashrc`` or ``.zshrc``:

.. code:: shell

    eval "$(ntfy shell-integration)"

By default it will only send notifications for commands lasting longer than 10
seconds and if the terminal is focused. Terminal focus works on X11(Linux) and
with Terminal.app and iTerm2 on MacOS. Both options can be configured via the
``--longer-than`` and ``--foreground-too`` options.

To avoid unnecessary notifications when running interactive programs, programs
listed in ``AUTO_NTFY_DONE_IGNORE`` don't generate notifications. For example:

.. code:: shell

    export AUTO_NTFY_DONE_IGNORE="vim screen meld"

Extras
~~~~~~
``ntfy`` can also a has a few features that require extra dependencies.
    * ``nfty done -p $PID`` requires installing as ``ntfy[pid]``
    * XMPP requires installing as ``ntfy[XMPP]``
    * Telegram requires installing as ``ntfy[telegram]``

emojis, Telegram and xmpp are extras.

Configuring ``ntfy``
--------------------

``ntfy`` is configured with a YAML file stored at ``~/.config/ntfy/ntfy.yml``

Backends
~~~~~~~~

The backends key specifies what backends to use by default. Each backend has
its own configuration, stored in a key of its own name. For example:

.. code:: yaml

    ---
    backends:
        - pushover
        - simplepush
        - linux
        - xmpp
    pushover:
        user_key: hunter2
    pushbullet:
        access_token: hunter2
    simplepush:
        key: hunter2
    xmpp:
         jid: "user@gmail.com"
         password: "xxxx"
         mtype: "chat"
         recipient: "me@jit.si"

If you want mulitple configs for the same backend type, you can specify any
name and then specify the backend with a backend key. For example:

.. code:: yaml

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
    * ``api_token`` - use your own application token
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

`Simplepush <https://simplepush.io>`_ - ``simplepush``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required parameter:
    * ``key`` - Your Simplepush key, created by installing the Android App (no registration required) at https://simplepush.io

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

Require extras, install like this: ``pip install ntfy[xmpp]``.

To verify the SSL certificates offered by a server:
path_to_certs = "path/to/ca/cert"

Without dnspython library installed, you will need
to specify the server hostname if it doesn't match the jid.

For example, to use Google Talk you would need to use:
hostname = 'talk.google.com'

Specify port if other than 5222.
NOTE: Ignored without specified hostname

`Telegram <https://telegram.org>`_ - ``telegram``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Require extras, install like this: ``pip install ntfy[telegram]``.

Requires ``ntfy`` to be installed as ``ntfy[telegram]``. This backend is
configured the first time you will try to use it: ``ntfy -b telegram send
"Telegram configured for ntfy"``.

`Pushjet <https://pushjet.io/>`_ - ``pushjet``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required parameter:
    * ``secret`` - The Pushjet service secret token, created with http://docs.pushjet.io/docs/creating-a-new-service

Optional parameters:
    * ``endpoint`` - custom Pushjet API endpoint
        (defaults to https://api.pushjet.io)
    * ``level`` - The importance level from 1(low) to 5(high)
    * ``link``

`Notifico <https://n.tkte.ch/>`_ - ``notifico``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required parameter:
    * ``webhook`` - The webhook link, created at https://n.tkte.ch/
                    (choose ``Plain Text`` service when creating the webhook)

`Linux Desktop Notifications <https://developer.gnome.org/notification-spec/>`_ - ``linux``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Works via `dbus`, works with most DEs like Gnome, KDE, XFCE and with libnotify.

You will need to install some font that supports emojis (in Debian `fonts-symbola` or Gentoo `media-fonts/symbola`).

Windows Desktop Notifications - ``win32``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Uses ``pywin32``.

Mac OS X Notification Center - ``darwin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Requires ``ntfy`` to be installed globally (not in a virtualenv).

Other options
~~~~~~~~~~~~~

Title is configurable with the `title` key in the config. Example:

.. code:: yaml

    ---
    title: Customized Title


Backends ToDo
~~~~~~~~~~~~~
-  `Prowl <http://www.prowlapp.com>`_
-  `Airgram <http://www.airgramapp.com>`_
-  `Pushalot <https://pushalot.com>`_
-  `Boxcar <https://boxcar.io>`_
-  `Instapush <https://instapush.im>`_

Testing
-------

.. code:: shell

    python setup.py test

Contributors
------------
- `dschep <https://github.com/dschep>`_ - Maintainer & Lead Developer
- `danryder <https://github.com/danryder>`_ - XMPP Backend & emoji support
- `oz123 <https://github.com/oz123>`_ - Linux desktop notification improvements
- `schwert <https://github.com/schwert>`_ - PushJet support
- `rahiel <https://github.com/rahiel>`_ - Telegram support
- `tymm <https://github.com/tymm>`_ - Simplepush support
- `jungle-boogie <https://github.com/jungle-boogie>`_ - Documentation updates
- `tjbenator <https://github.com/tjbenator>`_ - Advanced Pushover options
- `mobiusklein <https://github.com/mobiusklein>`_ - Win32 Bugfix
- `rcaloras <https://github.com/rcaloras>`_ - Creator of `bash-prexec`, without which there woudn't be bash shell integration for `ntfy`
- `eightnoteight <https://github.com/eightnoteight>`_ - Notifico support
