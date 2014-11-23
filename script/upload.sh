#!/usr/bin/env sh

python $(dirname $0)/../setup.py sdist bdist_wheel upload -r $1