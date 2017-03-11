#!/usr/bin/env bash

sudo apt-get install -y python-pip python3-dev
sudo pip install --upgrade virtualenv

virtualenv -p python3 venv

