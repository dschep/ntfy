import sys
from os import path


vendor_path = path.abspath(path.split(__file__)[0])

if vendor_path not in sys.path:
    sys.path.append(vendor_path)
