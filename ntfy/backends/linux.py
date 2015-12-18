from subprocess import call

def notify(subject, config, message=None, device=None):
    argv = ['notify-send', subject]
    if message:
        argv.append(message)
    retcode = call(argv)

    if retcode:
        raise EnvironmentError('"{}" returned {}'.format(argv, retcode))
