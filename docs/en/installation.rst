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

.. warning:: Replace `/dev/null` by your real device name !

.. code-block:: bash

    sudo dcfldd if=2013-12-20-wheezy-raspbian.img of=/dev/null bs=1m sizeprobe=if status=on
    sync

.. note:: If you don't have ``dfcldd``, the classic alternative ``sudo dd if=2013-12-20-wheezy-raspbian.img of=/dev/null bs=1m && sync`` will work.

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
    sudo apt-get -y install python3-setuptools python3-pip python-virtualenv

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

* Enable Watchdog (optional)

.. code-block:: bash

    echo "bcm2708_wdog" | sudo tee -a /etc/modules
    sudo apt-get install watchdog
    sudo update-rc.d watchdog defaults
    sudo sed -i 's/^#watchdog-device.*/watchdog-device = \/dev\/watchdog/' /etc/watchdog.conf
    sudo /etc/init.d/watchdog start

.. warning:: The watchdog doesn't seem to work properly.

* Reboot at this point to activate i2c & watchdod

.. code-block:: bash

   sudo reboot

Griotte
=======

Installation from checkout
--------------------------

.. code-block:: bash

    git clone https://github.com/erasme/griotte.git
    git checkout devel
    cd griotte
    make install.prod

or if you need development libraries :

.. code-block:: bash

    make install.dev

If you'd rather work in a virtualenv :

.. code-block:: bash

    make virtual.dev

or
    make virtual.prod

.. warning:: Running in a virtualenv may cause trouble unless you have installed
             as root. Since RPIO requires you to be root and virtualenv doesn't
             work when sudo'ing, you'll have to issue `make virtual....` as root.
             You still can work fine under virtualenv if you don't use
             `bin/gpio`.

If you get an error using `make virtual.dev` or `make virtual.prod`, try
regenerating virtualenv bootstrap scripts :

.. code-block:: bash

    python create-bootstrap.py

and re-run `make virtual.devel` or `make virtual.prod`.

Then, activate virtualenv :

.. code-block:: bash

    source griotte/tools/env.sh

.. note:: You might need to adjust your python3 path in the top-level Makefile.
.. note:: This step is required everytime you log in.

You can list all available targets in the makefile by invoking `make` without
arguments :

* **clean** : cleans generated files, including doc
* **cov** : runs test suite with coverage
* **virtual.dev** : installs in a virtualenv with developpment dependencies
* **virtual.prod** : installs in a virtualenv with production dependencies
* **install.dev** : installs system-wide with developpment dependencies
* **install.prod** : installs system-wide with production dependencies
* **doc,docs** : generates documentation
* **rtfm** : opens local documentation in browser
* **tests** : runs test suite

Services
--------

If you use virtualenv, the prefix will be `griotte/bin/` (assuming you're at the
top-level directory of the checkout).

If you've installed system-wide, it's `/usr/local/bin`

Start the server with :

.. code-block:: bash

    <prefix>/server

Start the required handlers like so :

.. code-block:: bash

    <prefix>/storage
    <prefix>/adc
    <prefix>/gpio
    <prefix>/multimedia
    <prefix>/director

Head to [the server](http://localhost:8888) (change localhost if you installed
it somewhere else), and start playing with the application !

If you want to install an AP on you Pi, check out :doc:`installation_optional`.
