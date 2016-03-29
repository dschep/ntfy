#!/bin/bash

rm -r ntfy/vendor
git checkout ntfy/vendor/{.gitignore,__init__.py}
pip install --system --target=ntfy/vendor -r requirements.txt
