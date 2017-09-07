#!/usr/bin/env bash

# Enable backports
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B48AD6246925553
echo 'deb http://httpredir.debian.org/debian jessie-backports main contrib non-free' | sudo tee -a /etc/apt/sources.list.d/jessie-backports.list
sudo apt-get update

# Install certbot
sudo apt-get install -y certbot -t jessie-backports

sudo certbot certonly --webroot -w /var/www/smrty.net -d smrty.net -d www.smrty.net

sudo certbot renew

#sudo certbot certonly --webroot -w /var/www/smrty.net -d smrty.net -d www.smrty.net
#Saving debug log to /var/log/letsencrypt/letsencrypt.log
#Enter email address (used for urgent renewal and security notices) (Enter 'c' to
#cancel):gin.mail@gmail.com
#Starting new HTTPS connection (1): acme-v01.api.letsencrypt.org
#
#-------------------------------------------------------------------------------
#Please read the Terms of Service at
#https://letsencrypt.org/documents/LE-SA-v1.1.1-August-1-2016.pdf. You must agree
#in order to register with the ACME server at
#https://acme-v01.api.letsencrypt.org/directory
#-------------------------------------------------------------------------------
#(A)gree/(C)ancel: A
#Obtaining a new certificate
#Performing the following challenges:
#http-01 challenge for smrty.net
#http-01 challenge for www.smrty.net
#Using the webroot path /var/www/smrty.net for all unmatched domains.
#Waiting for verification...
#Cleaning up challenges
#Generating key (2048 bits): /etc/letsencrypt/keys/0000_key-certbot.pem
#Creating CSR: /etc/letsencrypt/csr/0000_csr-certbot.pem
#
#IMPORTANT NOTES:
# - Congratulations! Your certificate and chain have been saved at
#   /etc/letsencrypt/live/smrty.net/fullchain.pem. Your cert will
#   expire on 2017-10-22. To obtain a new or tweaked version of this
#   certificate in the future, simply run certbot again. To
#   non-interactively renew *all* of your certificates, run "certbot
#   renew"
# - If you lose your account credentials, you can recover through
#   e-mails sent to gin.mail@gmail.com.
# - Your account credentials have been saved in your Certbot
#   configuration directory at /etc/letsencrypt. You should make a
#   secure backup of this folder now. This configuration directory will
#   also contain certificates and private keys obtained by Certbot so
#   making regular backups of this folder is ideal.
# - If you like Certbot, please consider supporting our work by:
#
#   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
#   Donating to EFF:                    https://eff.org/donate-le