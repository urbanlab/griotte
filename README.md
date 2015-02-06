```
       ______________________________________________________________________________________________
      ___/\/\/\/\/\__/\/\/\/\/\____/\/\/\/\____/\/\/\/\____/\/\/\/\/\/\__/\/\/\/\/\/\__/\/\/\/\/\/\_
     _/\/\__________/\/\____/\/\____/\/\____/\/\____/\/\______/\/\__________/\/\______/\___________
    _/\/\__/\/\/\__/\/\/\/\/\______/\/\____/\/\____/\/\______/\/\__________/\/\______/\/\/\/\/\___  
   _/\/\____/\/\__/\/\__/\/\______/\/\____/\/\____/\/\______/\/\__________/\/\______/\/\_________
  ___/\/\/\/\/\__/\/\____/\/\__/\/\/\/\____/\/\/\/\________/\/\__________/\/\______/\/\/\/\/\/\_
 ______________________________________________________________________________________________  

```


Description
-------------

Griotte is a framework that turns a Raspberry Pi into a programmable multimedia player.

Associated with a RaspiOMix interface and sensors (temperature, distance, RFID, ..., you name it), the player can react to external events, activate external devices, drive lights via DMX, ...

While RaspiOMix uses SeeedStudio's Grove system, giving access to a wide range of sensors and actuators, any 3.3v/5v sensor can be used.

Griotte can play scenarios written with Blockly simply by dragging and dropping blocks.

Applications include museum players (that can react to visitors for instance), educational tools (learning about programming or sensors), home automation, lighting systems, ...


Installation
-------------

  0. configure your raspberry pi

		sudo raspi-config
		> 8 Advanced Options
		> A6 I2C
		> yes

		sudo nano /etc/modules
		#add the folowing line
		i2c-dev
		#save and exit

		#install i2ctools and reboot
		sudo apt-get install i2c-tools
		sudo apt-get update
		sudo adduser pi i2c
		sudo reboot

  1bis. (temporary) Install missing pkg

  		sudo apt-get install libfreeimage-dev

  1ter. Install ftdi driver for ENTTEC DMX USB PRO

  		follow the instructions at http://www.ftdichip.com/Drivers/D2XX.htm
  		and then copy ftd2xx.h and WinTypes.h to /usr/local/include directory
  		OR
  		(clone the node ftdi module (https://github.com/KABA-CCEAC/node-ftdi) and run install.sh that will do the math
  		for you.)

  		NB : if you have ftdi_sio installed you might need to remove it for the DMX USB PRO to work properly
  		(sudo nano /etc/modprobe.d/raspi-blacklist.conf)

  1. install node.js

  	create a node directory and download the last arm distribution
  	in this directory

		cd /home/pi
  		mkdir node
  		cd ./node
  		wget http://node-arm.herokuapp.com/node_latest_armhf.deb

  	Install the downloaded package

  		sudo dpkg -i node_latest_armhf.deb

  	Once the package installed you should be able to run node typing "node"
  	and execute a console.log("hello baby") in interactive mode

  2. clone HController from GitHub

		cd /home/pi
		git clone --recursive -b griotte https://github.com/erasme/griotte.git

  3. install forever

		sudo npm install forever -g

  4. Get Started :

  	cd griotte
    ./startup.sh

```

C
