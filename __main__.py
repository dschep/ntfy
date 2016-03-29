#!/usr/bin/python2
__requires__ = 'ntfy'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('ntfy', 'console_scripts', 'ntfy')()
    )
