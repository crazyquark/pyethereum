#!/bin/bash

sudo pip install virtualenv
virtualenv venv

source venv/bin/activate

pip install pytest

export SED=/usr/local/Library/Homebrew/shims/super/sed
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" python setup.py install


