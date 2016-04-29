#!/bin/bash

rm -rf build/zipapp
mkdir -p build/zipapp dist
cp __main__.py build/zipapp
pip install --target=build/zipapp -r requirements.txt .
touch build/zipapp/ruamel/__init__.py  # ruamel is a namespace package
find build/zipapp/ -name '*.pyc' -delete
find build/zipapp/ -name '*.so' -delete
find build/zipapp/ -name '*.pth' -delete
python3 -m zipapp -h &> /dev/null && \
    python3 -m zipapp -o dist/ntfy --python /usr/bin/python build/zipapp || \
    echo 'zipapp only supported in Python3.5, zip build/zipapp yourself'
