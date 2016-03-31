#!/bin/bash

rm -rf build/zipapp
mkdir -p build/zipapp dist
cp __main__.py build/zipapp
pip install --target=build/zipapp -r requirements.txt .
python -m zipapp -h &> /dev/null && \
    python -m zipapp -o dist/ntfy --python /usr/bin/python build/zipapp || \
    echo 'zipapp only supported in Python3.5, zip build/zipapp yourself'
