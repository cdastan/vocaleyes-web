#!/bin/bash

APP_DIR="./app"
# CIRCUS_FILE="/etc/circus.ini"
# CIRCUS_CONFIG="conf/circus.ini"


# ----------------------
# Install virtualenv
# ----------------------
if [ ! -e venv ]; then
    #pyvenv venv # python3 (broken on Ubuntu 14.04)
    #virtualenv  # python2

    # Ubuntu 14.04 is broken, recipe
    # to fix this bellow
    pyvenv-3.4 --without-pip venv
    source ./venv/bin/activate
    wget https://pypi.python.org/packages/source/s/setuptools/setuptools-3.4.4.tar.gz
    tar -vzxf setuptools-3.4.4.tar.gz
    cd setuptools-3.4.4
    python setup.py install
    cd ..
    wget https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz
    tar -vzxf pip-1.5.6.tar.gz
    cd pip-1.5.6
    python setup.py install
    cd ..
    deactivate
    source ./venv/bin/activate
fi
source venv/bin/activate

# Install reqs
pip install -r "$APP_DIR/requirements.txt"

deactivate


# ----------------------
# Other
# ----------------------
