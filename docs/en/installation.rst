Installation from scratch
*************************

Whole scoop on installing a full featured Griotte device the hard way, with AP
capability (no ethernet bridging or forwarding though).

Image & base config
===================

* Download Raspbian image from http://www.raspberrypi.org/downloads
* Uncompress with

.. code-block:: bash

    unzip 2013-12-20-wheezy-raspbian.zip

* Dump to SD card

.. code-block:: bash

    sudo dcfldd if=2013-12-20-wheezy-raspbian.img of=/dev/sdc bs=1m sizeprobe=if status=on
    sync

.. note:: If you don't have ``dfcldd``, the classic alternative ``sudo dd if=2013-12-20-wheezy-raspbian.img of=/dev/sdc bs=1m && sync`` will work.

* Boot Pi
* Change keyboard if needed, e.g. for French :

.. code-block:: bash

    cat | sudo tee /etc/default/keyboard<<EOF > /dev/null
    XKBMODEL="pc105"
    XKBLAYOUT="fr"
    XKBVARIANT=""
    XKBOPTIONS="compose:lwin,terminate:ctrl_alt_bksp"

    BACKSPACE="guess"
    EOF

    sudo service keyboard-setup restart

* Install some prereqs

.. code-block:: bash

    sudo apt-get update
    sudo apt-get -y install python-setuptools python3-pip python-virtualenv dnsmasq

* Apply updates

.. code-block:: bash

    sudo apt-get -y upgrade
    sudo rpi-update
    sync && sudo reboot

Install specific omxplayer version
==================================

.. code-block:: bash

    wget http://griotte.erasme.org/downloads/omxplayer_latest.deb
    sudo dpkg -i omxplayer_latest.deb

Devices
=======

* Enable spi & i2c

.. code-block:: bash

    sudo rm /etc/modprobe.d/raspi-blacklist.conf
    echo "i2c-dev" | sudo tee -a /etc/modules
    sudo apt-get install -y i2c-tools
    sudo usermod -aG i2c pi
    echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c"' | sudo tee /etc/udev/rules.d/10-local_i2c_group.rules

* Enable Watchdog

.. code-block:: bash

    echo "bcm2708_wdog" | sudo tee -a /etc/modules
    sudo apt-get install watchdog
    sudo update-rc.d watchdog defaults
    sudo sed -i 's/^#watchdog-device.*/watchdog-device = \/dev\/watchdog/' /etc/watchdog.conf
    sudo /etc/init.d/watchdog start

.. warning:: The watchdog doesn't seem to work properly.

Griotte
=======

Installation
------------

.. code-block:: bash

    git clone https://github.com/erasme/griotte.git
    cd griotte
    make production

or if you need development libraries :

.. code-block:: bash

    make devel

Then, activate virtualenv :

.. code-block:: bash

    source griotte/tools/env.sh

.. note:: You might need to adjust your python3 path in the top-level Makefile.

You can list all available targets in the makefile by invoking `make` :

* **clean** : cleans generated files, including doc
* **cov** : runs test suite with coverage
* **dev,devel** : installs developpment dependencies
* **doc,docs** : generates documentation
* **prod,production** : installs production dependencies
* **rtfm** : opens local documentation in browser
* **tests** : runs test suite

Services
--------

Start the server with :

.. code-block:: bash

    griotte/bin/server

Start the required handlers like so :

.. code-block:: bash

    griotte/bin/storage
    griotte/bin/adc
    griotte/bin/gpio
    griotte/bin/multimedia
    griotte/bin/director

Head to [the server](http://localhost:8888) (change localhost if you installed
it somewhere else), and start playing with the application !

If you want to install an AP on you Pi, check out :doc:`installation_optional`.
