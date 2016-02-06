Configuring ``ntfy``
====================

``ntfy`` is configured with a YAML file stored at ``~/.ntfy.yml``

Backends
--------

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

Note: v0.2.1 and older supported only a single backend, to support old configuration files ntfy will still accept a single backend (a string instead of a list of strings) with the key 'backend'.

The available backends are in `ntfy.backends <ntfy.backends.html>`_,
include only the module name in your config (eg: ``pushbullet`` not
``ntfy.backends.pushbullet``).
