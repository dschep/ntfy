#!/bin/bash

rm -rf build/zipapp
mkdir -p build/zipapp dist
cp __main__.py build/zipapp
pip install --target=build/zipapp -r requirements.txt .
type -P python3.5 &> /dev/null && \
	python3 -m zipapp -o dist/ntfy --python /usr/bin/python2.7 build/zipapp
