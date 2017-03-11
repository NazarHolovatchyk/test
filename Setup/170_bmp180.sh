#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install git build-essential python-dev python-smbus
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP

virtualenv venv
. venv/bin/activate
python setup.py install

# SUDO REQUIRED !!!
cd examples
sudo python simpletest.py

