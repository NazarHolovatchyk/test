#!/usr/bin/env bash

# GPIO
sudo apt-get update
sudo apt-get install -y python-dev python-rpi.gpio


# I2C
sudo apt-get install -y python-smbus i2c-tools

sudo raspi-config
# Enable i2C

sudo echo "i2c-bcm2708" >> /etc/modules
sudo echo "i2c-dev" >> /etc/modules
sudo echo "" >> /etc/modules

# If exists - comment in /etc/modprobe.d/raspi-blacklist.conf
# blacklist spi-bcm2708
# blacklist i2c-bcm2708

# If you are running a recent Raspberry Pi (3.18 kernel or higher)
#sudo echo "dtparam=i2c1=on" >> /boot/config.txt
#sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt

sudo reboot

sudo i2cdetect -y 1


# SPI
# Comment backlist in sudo nano /etc/modprobe.d/raspi-blacklist.conf
# blacklist spi-bcm2708

sudo reboot

# List SPI devices with
ls -l /dev/spidev*

