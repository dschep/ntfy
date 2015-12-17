# `ntfy` - A utility for sending notifications

`ntfy` is a command line utility (and to a degree, python library) for sending
push notifications. Unlike many existing utilities for Pushover or Pushbullet,
it supports multiple backends.

# Backends
### Supported
 * [Pushover](https://pushover.net)
 * [Pushbullet](https://pushbullet.com)

### Planned/Possible
 * [Prowl](http://www.prowlapp.com)
 * [Airgram](http://www.airgramapp.com)
 * [Pushjet](https://pushjet.io)
 * [Pushalot](https://pushalot.com)
 * [Boxcar](https://boxcar.io)
 * [Instapush](https://instapush.im)
 * Mac OS X Notification Center
 * Linux Desktop Notifications (notify-send/PyNotify)
 * Windows Desktop Notifications?

## Config
`ntfy` is configured via a json config file stored at `~/.ntfy.json`. It
requires at minimum 2 keys: backend & a config for that backend.

### Example Config
```
{
    "backend": "pushbullet",
    "access_token": "<redacted>"
}
```
