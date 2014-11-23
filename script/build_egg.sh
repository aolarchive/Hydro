#!/usr/bin/env sh

#python $(dirname $0)/../setup.py bdist_wheel
python $(dirname $0)/../setup.py test
python $(dirname $0)/../setup.py sdist bdist_egg
