#!/bin/bash
set -e

sudo apt-get install -y apt-transport-https
sudo sh -c "echo 'deb https://apt.datadoghq.com/ stable main' > /etc/apt/sources.list.d/datadog.list"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7A7DA52
sudo apt-get update
sudo apt-get install -y datadog-agent
