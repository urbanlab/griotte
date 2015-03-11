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

  1. clone Griotte from GitHub

		git clone --recursive -b v2 https://github.com/erasme/griotte.git

  3. Install dependencies (Raspbian/Debian script), you must reboot once completed.

		cd griotte
		sudo ./install_dependencies.sh
		sudo reboot

  4. Get Started

  	cd griotte
    	./startup.sh
    	
  5. Use
  	
	You can access the web interface via your webbrowser at
		http://<your pi IP>:8080
	And begin to write your own scenarios !


Credits
--------

The Griotte Project is supported by Erasme, Lyon - France

Griotte v2 has been fully re-coded by @AlainBarthelemy from the [Hemisphere-Project](https://github.com/Hemisphere-Project) Team.

Griotte v2 run with Node.JS

Griotte v2 use external modules to work:

- [HPlayer](https://github.com/Hemisphere-Project/HPlayer) to playback multimedia cotents
- [HDmx](https://github.com/Hemisphere-Project/HDmx) to interface Enttec DMXUSB Pro 
- [MCP3424](https://github.com/x3itsolutions/mcp3424) to interface MCP3424 4Channel Delta Sigma ADC 
- a bunch of Node.JS modules (firmata, osc, i2c, rpio, serialport, http-server, socket.io, ...)
- some common Web frameworks and libraries (Jquery, Bootstrap, ...)

