#!/usr/bin/env bash

cd ~/domoticz
virualenv venv
source venv/bin/activate
cd ~
git clone https://github.com/mjg59/python-broadlink.git
cd python-broadlink
python setup.py develop

scp domoticz/scripts/* pi@192.168.1.200
ssh pi@192.168.1.200
mv ~/scripts domoticz

cd ~
~/domoticz/venv/bin/python ~/domoticz/scripts/python/broadlink_cli.py -i 192.168.1.201 -m B4:43:0D:FB:C9:F5 -c JgBIAAABJpMTEhMREzcTERMSExETEhMREzcTNhMREzcSNxM2EzYTNhMSExETEhM2ExITERMSExITNhM2EzYTEhM2EzYTNhM2EwANBQ==