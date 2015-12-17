# About `ntfy`

`ntfy` is a command line utility (and to a degree, python library) for sending
push notifications. Unlike many existing utilities for Pushover or Pushbullet,
it supports multiple backends.

## Usage
```
usage: ntfy [-h] [-t TITLE] [-d DEVICE] [-c CONFIG_FILE] [-b BACKEND] ...

Send push notification

positional arguments:
  MESSAGE               notification message

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        a title for the notification (default:
                        dschep@endgames)
  -d DEVICE, --device DEVICE
                        device to notify
  -c CONFIG_FILE, --config CONFIG_FILE
                        config file to use (default: ~/.ntfy.json)
  -b BACKEND, --backend BACKEND
                        override backend specified in config
```

## `ntfy-done` - A utility for notifying you when a command finishes
`ntfy-done` is a CLI utility for sending a notification when a command
finishes. Instead of passing a message as the extra positional arguments,
provide the command you wish to run.

### Example:
```
ntfy-done sleep 10
```


# Backends
 - [x] [Pushover](https://pushover.net)
 - [x] [Pushbullet](https://pushbullet.com)
 - [ ] [Prowl](http://www.prowlapp.com)
 - [ ] [Airgram](http://www.airgramapp.com)
 - [ ] [Pushjet](https://pushjet.io)
 - [ ] [Pushalot](https://pushalot.com)
 - [ ] [Boxcar](https://boxcar.io)
 - [ ] [Instapush](https://instapush.im)
 - [ ] Mac OS X Notification Center
 - [ ] Linux Desktop Notifications (notify-send/PyNotify)
 - [ ] Windows Desktop Notifications?

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
