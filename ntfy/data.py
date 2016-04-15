from os import path, makedirs, stat
from pkgutil import get_data
from sys import argv

from appdirs import user_data_dir

ntfy_data_dir = user_data_dir('ntfy', 'dschep')
if not path.isdir(ntfy_data_dir):
    makedirs(ntfy_data_dir)


class icon(object):
    png = None
    ico = None


for fmt in ['png', 'ico']:
    icon_path = path.abspath(path.join(ntfy_data_dir, 'icon.' + fmt))
    setattr(icon, fmt, icon_path)
    if not path.isfile(icon_path) or stat(argv[0]).st_mtime > stat(
            icon_path).st_mtime:
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(get_data('ntfy', 'icon.' + fmt))

scripts = {}
for script in ['auto-ntfy-done.sh', 'bash-preexec.sh']:
    script_path = path.abspath(path.join(ntfy_data_dir, script))
    scripts[script] = script_path
    if not path.isfile(script_path) or stat(argv[0]).st_mtime > stat(
            script_path).st_mtime:
        with open(script_path, 'wb') as script_file:
            script_file.write(get_data('ntfy', path.join('shell_integration',
                                                         script)))
