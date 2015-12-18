from subprocess import call
from os import path

ICON = path.abspath(path.join(path.split(path.split(__file__)[0])[0],
                              'icon.png'))

def notify(subject, config, message=None, device=None):
    argv = ['notify-send', '-i', ICON, subject]
    if message:
        argv.append(message)
    retcode = call(argv)

    if retcode:
        raise EnvironmentError('"{}" returned {}'.format(argv, retcode))
