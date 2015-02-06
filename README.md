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
		git clone --recursive -b griotte https://github.com/Hemisphere-Project/HController.git

  3. install forever

		sudo npm install forever -g

  4. Get Started :

  	cd griotte
    ./startup.sh


OSC Messages
-------------

	/play [<path1>] [<path2>] ...       : Play the file (or dir) list in order
	/playloop [<path1>] [<path2>] ...   : Same as play with playlist loop
	/volume <0:100>     : Set volume from 0 to 100
	/blur <0:100>       : Set blur level from 0 to 100
	/zoom <0:100>       : Set zoom from 0 to 100%
	/stop           : Stop and rewind the current video file
	/pause          : Pause the video file
	/resume         : Resume the paused file
	/next           : Play the next file in the list
	/prev           : Play the previous file in the list
	/mute           : Mute the sound of the video
	/unmute         : Unmute the sound of the video
	/loop           : Enable looping for the current playlist
	/unloop         : Disable looping for the current playlist
	/info           : Toggle media info window (disabled)
	/quit           : Exit the player

About config
-------------

Here is a brief description of the globalconfig.json parameters. You can change them at your convinience.
```
ModuleManager
	.playlistAutoLaunch (true|false) Do we launch HPlayer in playlist mode
MediaManager
	.mediaDir (pathToDir) Path to the directory where the media are stored
	.USBDir (pathToDir) Path the USB directory where there's media you want to copy (typically /media/usb for the latest drive mounted with usbmount)
OSCInterface (obj) Parameter of the OSCInterface
RemoteInterface (?) Nothing here. Will welcome parameters for a remote control if the feature is developped sometime
WebServer
	.root_dir (pathToDir) path to the web root dir, often named www...
	.port (int) the port used by webserver
	.refreshStatusPeriod (int) how often we query the HPlayer for status upade (in ms)

ProcessManager
	.HPlayerPath (pathToBin) location of the HPlayer binary
HPlayer (obj) default parameters of the HPlayer
SerialInterface
	.baudRate (int) We use serial to communicate with an arduino board sometime..

IcePicker (obj) Some creepy watchdog who kills HPlayer when frozen. Will be removed upon lake placid of full stability.
```

Credits
-------------

HController is developped by the Hemisphere-Project Team

    ++ Thomas Bohl ++
    ++ Alain Barthelemy ++
    ++ Jeremie Forge ++
