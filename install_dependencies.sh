#!/bin/bash
sudo apt-get update

#I2C tools
sudo apt-get install i2c-tools -y
sudo adduser pi i2c

#HPLAYER libs
sudo apt-get install libfreeimage-dev -y

#INSTALL LAST NODE VERSION
wget http://node-arm.herokuapp.com/node_latest_armhf.deb
sudo dpkg -i node_latest_armhf.deb
rm node_latest_armhf.deb

#FOREVER
sudo npm install forever -g

#HDMX libs
sudo ./bin/HDmx/install.sh

#FINNISH
echo ' '
echo ' '
echo 'Installation finnished.. You should reboot now !'
