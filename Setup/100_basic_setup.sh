#!/usr/bin/env bash

sudo raspi-config

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y vim


sudo vim /etc/dhcpcd.conf
#========================= At the beginning
interface eth0
static ip_address=192.168.1.200/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
#=========================

# Local time
sudo cp /usr/share/zoneinfo/Europe/Kiev /etc/localtime
sudo reboot


