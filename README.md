# About `ntfy`

[![Version](https://img.shields.io/pypi/v/ntfy.svg?logo=data%3Aimage/svg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNDAiIGhlaWdodD0iMjQwIj48cGF0aCBmaWxsPSIjMzY3MWEyIiBkPSJNNjIuNDc2IDMzLjRjMC0xNi4zNiA0LjM4Ni0yNS4yNiAyOC42MDctMjkuNDk4IDE2LjQ0NC0yLjg4IDM3LjUyOC0zLjI0MiA1Ny4xOTMgMCAxNS41MzMgMi41NjQgMjguNjA3IDE0LjEzNCAyOC42MDcgMjkuNDk3djUzLjk3YzAgMTUuODMtMTIuNjkzIDI4Ljc5NS0yOC42MDcgMjguNzk1SDkxLjA4M2MtMTkuNDEgMC0zNS43NyAxNi41NS0zNS43NyAzNS4yNnYyNS44OTVIMzUuNjVjLTE2LjYzNiAwLTI2LjMyLTExLjk5My0zMC4zODgtMjguNzc2LTUuNDktMjIuNTQ2LTUuMjU2LTM1Ljk4IDAtNTcuNTc0QzkuODE4IDcyLjEzNyAyNC4zNzUgNjIuMTk4IDQxLjAxIDYyLjE5OGg3OC42OHYtNy4yMDRINjIuNDc2VjMzLjR6Ii8%2BPHBhdGggZmlsbD0iI2ZmZDA0NiIgZD0iTTE3Ni44ODMgMjA2LjEyM2MwIDE2LjM2LTE0LjE5OCAyNC42NDQtMjguNjA3IDI4Ljc3Ni0yMS42NzggNi4yMy0zOS4wNzUgNS4yNzMtNTcuMTkzIDAtMTUuMTMtNC40MS0yOC42MDctMTMuNDE3LTI4LjYwNy0yOC43OHYtNTMuOTdjMC0xNS41MzMgMTIuOTQ3LTI4Ljc5OCAyOC42MDctMjguNzk4aDU3LjE5M2MxOS4wNSAwIDM1Ljc3LTE2LjQ2NSAzNS43Ny0zNS45OFY2Mi4xOTZoMjEuNDQ0YzE2LjY1NiAwIDI0LjQ5NiAxMi4zNzYgMjguNjA3IDI4Ljc3NyA1LjcyMiAyMi43OCA1Ljk3NiAzOS44MTcgMCA1Ny41NzQtNS43ODUgMTcuMjUtMTEuOTcyIDI4Ljc3Ny0yOC42MDcgMjguNzc3aC04NS44djcuMjA1aDU3LjE5M3YyMS41OXoiLz48L3N2Zz4%3D)](https://pypi.org/project/ntfy/)
[![Docs](http://readthedocs.org/projects/ntfy/badge/?version=latest)](http://ntfy.readthedocs.org/en/stable/?badge=latest)
[![SayThanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/dschep)

`ntfy` brings notification to your shell. It can automatically provide
desktop notifications when long running commands finish or it can send
push notifications to your phone when a specific command finishes.
Confused? This video demonstrates some of this functionality:

![image](https://raw.githubusercontent.com/dschep/ntfy/master/docs/demo.gif)

## Quickstart

``` shell
$ sudo pip install ntfy
$ ntfy send test
# send a notification when the command `sleep 10` finishes
# this sends the message '"sleep 10" succeeded in 0:10 minutes'
$ ntfy done sleep 10
$ ntfy -b pushover -o user_key t0k3n send 'Pushover test!'
$ ntfy -t 'ntfy' send "Here's a custom notification title!"
$ echo -e 'backends: ["pushover"]\npushover: {"user_key": "t0k3n"}' > ~/.ntfy.yml
$ ntfy send "Pushover via config file!"
$ ntfy done --pid 6379  # pid extra
$ ntfy send ":tada: ntfy supports emoji! :100:"  # emoji extra
# Enable shell integration
$ echo 'eval "$(ntfy shell-integration)"' >> ~/.bashrc
```

## Install

The install technique in the quickstart is the suggested method of
installation. It can be installed in a virtualenv, but with some
caveats: Linux notifications require `--system-site-packages` for the
virtualenv and OS X notifications don\'t work at all.

**:penguin: NOTE:** [Linux Desktop
Notifications](#linux-desktop-notifications---linux) require Python DBUS
bindings. See [here](#linux-desktop-notifications---linux) for more
info.

### Shell integration

`ntfy` has support for **automatically** sending notifications when long
running commands finish in bash and zsh. In bash it emulates zsh\'s
preexec and precmd functionality with
[rcaloras/bash-preexec](https://github.com/rcaloras/bash-preexec). To
enable it add the following to your `.bashrc` or `.zshrc`:

``` shell
eval "$(ntfy shell-integration)"
```

By default it will only send notifications for commands lasting longer
than 10 seconds and if the terminal is focused. Terminal focus works on
X11(Linux) and with Terminal.app and iTerm2 on MacOS. Both options can
be configured via the `--longer-than` and `--foreground-too` options.

To avoid unnecessary notifications when running interactive programs,
programs listed in `AUTO_NTFY_DONE_IGNORE` don\'t generate
notifications. For example:

``` shell
export AUTO_NTFY_DONE_IGNORE="vim screen meld"
```

### Extras

`ntfy` has a few features that require extra dependencies.

:   -   `ntfy done -p $PID` requires installing as
        `pip install ntfy[pid]`
    -   [emoji](https://en.wikipedia.org/wiki/Emoji) support requires
        installing as `pip install ntfy[emoji]`
    -   [XMPP](https://xmpp.org/) support requires installing as
        `pip install ntfy[xmpp]`
    -   [Telegram](https://telegram.org/) support requires installing as
        `pip install ntfy[telegram]`
    -   [Instapush](https://instapush.im/) support requires installing
        as `pip install ntfy[instapush]`
    -   [Slack](https://slack.com/) support requires installing as
        `pip install ntfy[slack]`
    -   [Slack Incoming webhook](https://slack.com/) - simpler slack
        implementation that doesn\'t have additional dependencies
    -   [Rocket.Chat](https://Rocket.Chat) support requires installing
        as `pip install ntfy[rocketchat]`

To install multiple extras, separate with commas: e.g.,
`pip install ntfy[pid,emoji]`.

## Configuring `ntfy`

`ntfy` is configured with a YAML file stored at `~/.ntfy.yml` or in
standard platform specific locations:

-   Linux - `~/.config/ntfy/ntfy.yml`
-   macOS - `~/Library/Application Support/ntfy/ntfy.yml`
-   Windows - `C:\Users\<User>\AppData\Local\dschep\ntfy.yml`

### Backends

The backends key specifies what backends to use by default. Each backend
has its own configuration, stored in a key of its own name. For example:

``` yaml
---
backends:
    - pushover
pushover:
    user_key: hunter2
pushbullet:
    access_token: hunter2
simplepush:
    key: hunter2
slack:
    token: slacktoken
    recipient: "#slackchannel"
xmpp:
     jid: "user@gmail.com"
     password: "xxxx"
     mtype: "chat"
     recipient: "me@jit.si"
```

If you want mulitple configs for the same backend type, you can specify
any name and then specify the backend with a backend key. For example:

``` yaml
---
pushover:
    user_key: hunter2
cellphone:
    backend: pushover
    user_key: hunter2
```

See the backends below for available backends and options. As of v2.6.0
`ntfy` also supports [3rd party backends](#3rd-party-backends)

### [Pushover](https://pushover.net) - `pushover`

Required parameters:

:   -   `user_key`

Optional parameters:

:   -   `sound`
    -   `priority`
    -   `expire`
    -   `retry`
    -   `callback`
    -   `api_token` - use your own application token
    -   `device` - target a device, if omitted, notification is sent to
        all devices
    -   `url`
    -   `url_title`
    -   `html`

### [Pushbullet](https://pushbullet.com) - `pushbullet`

Required parameter:

:   -   `access_token` - Your Pushbullet access token, created at
        <https://www.pushbullet.com/#settings/account>

Optional parameters:

:   -   `device_iden` - a device identifier, if omited, notification is
        sent to all devices
    -   `email` - send notification to pushbullet user with the
        specified email or send an email if they aren\'t a pushullet
        user

### [Simplepush](https://simplepush.io) - `simplepush`

Required parameter:

:   -   `key` - Your Simplepush key, created by installing the Android
        App (no registration required) at <https://simplepush.io>

Optional parameters:

:   -   `event` - sets ringtone and vibration pattern for incoming
        notifications (can be defined in the simplepush app)

### XMPP - `xmpp`

Requires parameters:

:   -   `jid`
    -   `password`
    -   `recipient`

Optional parameters

:   -   `hostname` (if not from jid)
    -   `port`
    -   `path_to_certs`
    -   `mtype`

Requires extras, install like this: `pip install ntfy[xmpp]`.

To verify the SSL certificates offered by a server: path_to_certs =
\"path/to/ca/cert\"

Without dnspython library installed, you will need to specify the server
hostname if it doesn\'t match the jid.

Specify port if other than 5222. NOTE: Ignored without specified
hostname

NOTE: Google Hangouts doesn\'t support XMPP since 2017

### [Telegram](https://telegram.org) - `telegram`

Requires extras, install like this: `pip install ntfy[telegram]`.

Requires `ntfy` to be installed as `ntfy[telegram]`. This backend is
configured the first time you will try to use it:
`ntfy -b telegram send "Telegram configured for ntfy"`.

### [Pushjet](https://pushjet.io/) - `pushjet`

Required parameter:

:   -   `secret` - The Pushjet service secret token, created with
        <http://docs.pushjet.io/docs/creating-a-new-service>

Optional parameters:

:   -   

        `endpoint` - custom Pushjet API endpoint

        :   (defaults to <https://api.pushjet.io>)

    -   `level` - The importance level from 1(low) to 5(high)

    -   `link`

### [Notifico](https://n.tkte.ch/) - `notifico`

Required parameter:

:   -   

        `webhook` - The webhook link, created at <https://n.tkte.ch/>

        :   (choose `Plain Text` service when creating the webhook)

### [Slack](https://slack.com) - `slack`

Requires extras, install like this: `pip install ntfy[slack]`.

Required parameter:

:   -   `token` - The Slack service secret token, either a legacy user
        token created at
        <https://api.slack.com/custom-integrations/legacy-tokens> or a
        token obtained by creating an app at
        <https://api.slack.com/apps?new_app=1> with `chat:write:bot`
        scope and linking it to a workspace.
    -   `recipient` - The Slack channel or user to send notifications
        to. If you use the `#` symbol the message is send to a Slack
        channel and if you use the `@` symbol the message is send to a
        Slack user.

[Slack Incoming Webhook](https://slack.com) - `slack_webhook`
\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~
Required parameter: \* `url` - the URL of the incoming webhook \*
`user` - The Slack channel or user to send notifications to

### [Instapush](https://instapush.im/) - `insta`

Requires extras, install like this `pip install ntfy[instapush]`.

Instapush does not support notification title. It sends template-driven
notifications, so you have to setup you events on the dashboard first.
The backend is called insta due to homonymy with the instapush python
wrapper

Required parameters:

:   -   `appid` - The application id
    -   `secret` - The application secret
    -   `event_name` - The instapush event to be used
    -   `trackers` - The array of trakers to use

Note on trackers: Trackers are placeholders for events (a sort of
notification template). If you defined more than one tracker in your
event you\'ll have to provide more messages. At the moment, the only way
to do so is to separate each message with a colon (:) character. You can
also escape the separator character: Example:

``` shell
ntfy -b insta send "message1:message2"
ntfy -b insta send "message1:message2\:with\:colons"
```

### [Prowl](https://www.prowlapp.com/) - `prowl`

Optional parameters:

:   -   `api_key`
    -   `provider_key`
    -   `priority`
    -   `url`

### [Linux Desktop Notifications](https://developer.gnome.org/notification-spec/) - `linux`

Works via [dbus]{.title-ref}, works with most DEs like Gnome, KDE, XFCE
and with libnotify.

The following dependecies should be installed.

``` shell
$ sudo apt install python-dbus # on ubuntu/debian
```

You will need to install some font that supports emojis (in Debian
[fonts-symbola]{.title-ref} or Gentoo
[media-fonts/symbola]{.title-ref}).

Optional parameters:

:   -   `icon` - Specifies path to the notification icon, empty string
        for no icon.
    -   `urgency` - Specifies the urgency level (low, normal, critical).
    -   `transient` - Skip the history (exp: the Gnome message tray)
        (true, false).
    -   `soundfile` - Specifies the notification sound file (e.g.
        /usr/share/sounds/notif.wav).
    -   `timeout` - Specifies notification expiration time level (-1 -
        system default, 0 - never expire).

### Windows Desktop Notifications - `win32`

Uses `pywin32`.

### Mac OS X Notification Center - `darwin`

Requires `ntfy` to be installed globally (not in a virtualenv).

### System log - `systemlog`

Uses the `syslog` core Python module, which is not available on Windows
platforms.

Optional parameters:

:   -   `prio` - Syslog priority level. Default is `ALERT`. Possible
        values are:

        -   EMERG
        -   ALERT
        -   CRIT
        -   ERR
        -   WARNING
        -   NOTICE
        -   INFO
        -   DEBUG

    -   `facility` - Syslog facility. Default is `LOCAL5`. Possible
        values are:

        -   KERN
        -   USER
        -   MAIL
        -   DAEMON
        -   AUTH
        -   LPR
        -   NEWS
        -   UUCP
        -   CRON
        -   SYSLOG
        -   LOCAL0
        -   LOCAL1
        -   LOCAL2
        -   LOCAL3
        -   LOCAL4
        -   LOCAL5
        -   LOCAL6
        -   LOCAL7

    -   `fmt` - Format of the message to be sent to the system logger.
        The title and the message are specified using the following
        placeholders:

        -   `{title}`
        -   `{message}`

        Default is `[{title}] {message}`.

### [Termux:API](https://play.google.com/store/apps/details?id=com.termux.api&hl=en) - `termux`

Requires the app to be install from the Play store and the CLI utility
be installed with `apt install termux-api`.

### [Pushalot](https://pushalot.com) - `pushalot`

Required parameter:

:   -   `auth_token` - Your private Pushalot auth token, found here
        <https://pushalot.com/manager/authorizations>

Optional parameters:

:   -   `source` - source of the notification
    -   `ttl` - message expire time in minutes (time to live)
    -   `url` - URL to include in the notifications
    -   `url_title` - visible URL title (ignored if no url specified)
    -   `image` - URL of image included in the notifications
    -   `important` - mark notifications as important
    -   `silent` - mark notifications as silent

### [Rocket.Chat](https://rocket.chat) - `rocketchat`

Requires extras, install like this: `pip install ntfy[rocketchat]`.

Required parameters:

:   -   `url` - URL of your Rocket.Chat instance
    -   `username` - login username
    -   `password` - login password
    -   `room` - room/channel name to post in

### [Matrix.org](https://matrix.org) - `matrix`

Requires extras, install like this: `pip install ntfy[matrix]`.

Required parameters:

:   -   `url` - URL of your homeserver instance
    -   `roomId` - room to post in
    -   `userId` - login userid
    -   `password` - login password
    -   `token` - access token

You must either specify `token`, or `userId` and `password`.

[Webpush](https://github.com/dschep/ntfy-webpush) - `ntfy_webpush`
\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~
Webpush support is provded by an external ntfy module, install like
this: `pip install ntfy ntfy-webpush`.

Required parameters:

:   -   `subscription_info` - A
        [PushSubscription](https://developer.mozilla.org/en-US/docs/Web/API/PushSubscription)
        Object
    -   `private_key` - the path to private key file or anything else
        that works with
        [pywebpush](https://github.com/web-push-libs/pywebpush).

For more info, see [ntfy-webpush]{#ntfy-webpush}
\<https://github.com/dschep/ntfy-webpush\>\`\_

### 3rd party backends

To use or implement your own backends, specify the full path of the
module as your backend. The module needs to contain a module with a
function called `notify` with the following signature:

``` python
def notify(title, message, **kwargs):
    """
    kwargs contains retcode if using ntfy done or ntfy shell-integration
    and all options in your backend's section of the config
    """
    pass
```

### Other options

Title is configurable with the [title]{.title-ref} key in the config.
Example:

``` yaml
---
title: Customized Title
```

### Backends ToDo

-   [Airgram](http://www.airgramapp.com)
-   [Boxcar](https://boxcar.io)

## Testing

``` shell
python setup.py test
```

## Contributors

-   [dschep](https://github.com/dschep) - Maintainer & Lead Developer
-   [danryder](https://github.com/danryder) - XMPP Backend & emoji
    support
-   [oz123](https://github.com/oz123) - Linux desktop notification
    improvements
-   [schwert](https://github.com/schwert) - PushJet support
-   [rahiel](https://github.com/rahiel) - Telegram support
-   [tymm](https://github.com/tymm) - Simplepush support
-   [jungle-boogie](https://github.com/jungle-boogie) - Documentation
    updates
-   [tjbenator](https://github.com/tjbenator) - Advanced Pushover
    options
-   [mobiusklein](https://github.com/mobiusklein) - Win32 Bugfix
-   [rcaloras](https://github.com/rcaloras) - Creator of
    [bash-prexec]{.title-ref}, without which there woudn\'t be bash
    shell integration for [ntfy]{.title-ref}
-   [eightnoteight](https://github.com/eightnoteight) - Notifico support
-   [juanpabloaj](https://github.com/juanpabloaj) - Slack support
-   [giuseongit](https://github.com/giuseongit) - Instapush support
-   [jlesage](https://github.com/jlesage) - Systemlog support
-   [sambrightman](https://github.com/sambrightman) - Prowl support
-   [mlesniew](https://github.com/mlesniew) - Pushalot support
-   [webworxshop](https://github.com/webworxshop) - Rocket.Chat support
-   [rhabbachi](https://github.com/rhabbachi) - transient option in
    Linux desktop notifications
-   [Half-Shot](https://github.com/Half-Shot) - Matrix support
