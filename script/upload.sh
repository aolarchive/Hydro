#!/usr/bin/env sh

python $(dirname $0)/../setup.py sdist bdist_egg upload -r $1
