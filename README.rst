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

``ntfy`` is a command line utility (and to a degree, python library) for
sending push notifications. It also can send a notification when a
program finishes.

Unlike many existing utilities for Pushover or Pushbullet, it supports
multiple backends.

Demo
----
.. image:: https://raw.githubusercontent.com/dschep/ntfy/master/docs/demo.gif

Install
-------

::

    sudo pip install ntfy

Note: It is suggested to globally (as indicated above, without a
virtualenv) install ntfy. It *can* be installed in a virtualenv, with caveats.
Linux notifications requires ``--system-site-packages`` to be used and OS X
notifications don't work at all.


Emoji Support :tada:
~~~~~~~~~~~~~~~~~~~~

``ntfy`` features emoji support, it is installable as an extra, just install
like this:

::

    sudo pip install ntfy[emoji]


XMPP Support
~~~~~~~~~~~~

The xmpp module requires sleekxmpp. To install this extra install ntfy like
this:

::

    sudo pip install ntfy[xmpp]


Usage
-----

::


    # send a notification
    ntfy send "Here's a notification!"

    # send a notification with custom title (default is $USER@$HOST:$PWD)
    ntfy -t 'ntfy' send "Here's a notification with a custom title!"

    # send a notification when the command `sleep 10` finishes
    # this send the message '"sleep 10" succeeded in 0:10 minutes'
    ntfy done sleep 10

Shell integration
~~~~~~~~~~~~~~~~~~~~
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


Backends
--------

Supported
~~~~~~~~~
-  `Pushover <https://pushover.net>`_
-  `Pushbullet <https://pushbullet.com>`_
-  XMPP
-  Linux Desktop Notifications
-  Windows Desktop Notifications
-  Mac OS X Notification Center

ToDo
~~~~
-  `Prowl <http://www.prowlapp.com>`_
-  `Airgram <http://www.airgramapp.com>`_
-  `Pushjet <https://pushjet.io>`_
-  `Pushalot <https://pushalot.com>`_
-  `Boxcar <https://boxcar.io>`_
-  `Instapush <https://instapush.im>`_

Configuring ``ntfy``
--------------------

``ntfy`` is configured with a YAML file stored at ``~/.ntfy.yml``

Backends
~~~~~~~~

The backends key specifies what backends to use by default. Each backend has
it's own configuration, stored in a key of it's own name. For example:

::

    ---
    backends:
        - pushover
        - linux
    pushover:
        user_key: hunter2
    pushbullet:
        access_token: hunter2

Note: versions prior to v1.0.0 used JSON instead of YAML.

The available backends are in `ntfy.backends <http://ntfy.readthedocs.org/en/stable/ntfy.backends.html>`_,
include only the module name in your config (eg: ``pushbullet`` not
``ntfy.backends.pushbullet``).

Testing
-------

::

    python setup.py test

Contributors
------------
- `dschep <https://github.com/dschep>`_ - Maintainer & Lead Developer
- `danryder <https://github.com/danryder>`_ - XMPP Backend & emoji support
