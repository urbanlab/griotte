************
Installation
************

Whole scoop on installing a full featured Griotte device with AP capability (no ethernet bridging or forwarding though).

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

Network
=======

* Disable IPv6 (unless you really need it)

.. code-block:: bash

    echo alias net-pf-10 off | sudo tee /etc/modprobe.d/ipv6.conf

AP (optional)
=============

You can turn your Raspberry Pi into an AP. This way, you don't need to hook with
ethernet to build scenarios in the application : just join the Raspberry's Wifi
network and play !

DWL-121 only (RealTek 8192cu)
-----------------------------

* Specific Hostapd (for DWL-121 only)

you need to find the drivers on the RealTek website (or googling). The exact
filename is ``rtl8192xc_usb_linux_v3.4.4_4749.20121105.zip``.

.. code-block:: bash

    unzip rtl8192xc_usb_linux_v3.4.4_4749.20121105.zip
    cd RTL8188C_8192C_USB_linux_v3.4.4_4749.20121105/wpa_supplicant_hostapd/
    unzip wpa_supplicant_hostapd-0.8_rtw_20120803.zip
    cd wpa_supplicant_hostapd-0.8/hostapd/
    make # takes 6.5 mins
    sudo make install
    echo "options 8192cu rtw_power_mgnt=0 rtw_enusbss=0" | sudo tee -a /etc/modprobe.d/8192cu.conf

* Create hostapd config

.. code-block:: bash

    cat | sudo tee /etc/hostapd.conf<<EOF > /dev/null
    interface=wlan0
    ssid=Raspeomix-Private
    channel=1
    #
    # WPA and WPA2 configuration
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=3
    wpa_passphrase=secretsecret
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    #
    # Hardware configuration
    driver=rtl871xdrv
    ieee80211n=1
    hw_mode=g
    device_name=RTL8192CU
    manufacturer=Realtek
    EOF


* Create hostapd startup script

.. code-block:: bash

    cat | sudo tee /etc/init.d/hostapd<<EOF > /dev/null
    ###################################################

    ### BEGIN INIT INFO
    # Provides:             hostapd
    # Required-Start:       $remote_fs
    # Required-Stop:        $remote_fs
    # Should-Start:         $network
    # Should-Stop:
    # Default-Start:        2 3 4 5
    # Default-Stop:         0 1 6
    # Short-Description:    Advanced IEEE 802.11 management daemon
    # Description:          Userspace IEEE 802.11 AP and IEEE 802.1X/WPA/WPA2/EAP
    #                       Authenticator
    ### END INIT INFO

    PATH=/sbin:/bin:/usr/sbin:/usr/bin
    DAEMON_SBIN=/usr/local/bin/hostapd
    DAEMON_CONF=/etc/hostapd/hostapd.conf
    NAME=hostapd
    DESC="advanced IEEE 802.11 management"
    PIDFILE=/var/run/hostapd.pid

    [ -x "$DAEMON_SBIN" ] || exit 0
    [ -n "$DAEMON_CONF" ] || exit 0

    DAEMON_OPTS="-B -P $PIDFILE $DAEMON_OPTS $DAEMON_CONF"

    . /lib/lsb/init-functions

    case "$1" in
      start)
            log_daemon_msg "Starting $DESC" "$NAME"
            start-stop-daemon --start --oknodo --quiet --exec "$DAEMON_SBIN" \
                    --pidfile "$PIDFILE" -- $DAEMON_OPTS >/dev/null
            log_end_msg "$?"
            ;;
      stop)
            log_daemon_msg "Stopping $DESC" "$NAME"
            start-stop-daemon --stop --oknodo --quiet --exec "$DAEMON_SBIN" \
                    --pidfile "$PIDFILE"
            log_end_msg "$?"
            ;;
      reload)
            log_daemon_msg "Reloading $DESC" "$NAME"
            start-stop-daemon --stop --signal HUP --exec "$DAEMON_SBIN" \
                    --pidfile "$PIDFILE"
            log_end_msg "$?"
            ;;
      restart|force-reload)
            $0 stop
            sleep 8
            $0 start
            ;;
      status)
            status_of_proc "$DAEMON_SBIN" "$NAME"
            exit $?
            ;;
      *)
            N=/etc/init.d/$NAME
            echo "Usage: $N {start|stop|restart|force-reload|reload|status}" >&2
            exit 1
            ;;
    esac

    exit 0
    EOF

    sudo chmod +x /etc/init.d/hostapd
    sudo update-rc.d hostapd defaults

Other models (e.g. DWA-140EU B2G)
---------------------------------

* Multiple SSIDs (optionnal)

Multiple SSID configuration can be interesting if you want to setup some captive
portal or admin interface. The full setup is not detailled here though, you're
on your own.

.. code-block:: bash

    cat | sudo tee /etc/network/interfaces<<EOF > /dev/null

    auto eth0
    iface eth0 inet dhcp

    auto wlan0
    # Hotplug will watch for this device and bring it up when connected.
    # Useful for USB devices
    allow-hotplug wlan0
    iface wlan0 inet static
     # Start hostapd if it is not running
     hostapd /etc/hostapd.conf
     address 192.168.166.1
     netmask 255.255.255.0
     ETHER
    EOF

    # Fix ethernet addres for BSSID alloc

    ETHER="02"$(ip link show wlan0 | grep ether | awk '{ print $2 }' | cut -c3-16)"0"
    sudo sed -i "s/ETHER/ pre-up ifconfig wlan0 hw ether $ETHER/" /etc/network/interfaces

.. warning:: Multiple SSIDs doesn't work with DWL-121 specific hostapd and many others

.. code-block:: bash

    cat | sudo tee /etc/hostapd.conf<<EOF > /dev/null

    driver=nl80211
    ieee80211n=1
    wmm_enabled=1
    ht_capab=[HT40+][SHORT-GI-40][MAX-AMSDU-3839]
    hw_mode=g
    interface=wlan0
    # Private
    bssid=02:26:5a:7f:af:00
    ssid=Griotte-Private
    channel=6
    # WPA and WPA2 configuration
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=3
    wpa_passphrase=supersecret
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    # Public
    bss=wlan0_0
    ssid=Griotte-Public
    EOF


DNSMasq
-------

.. code-block:: bash

interface=wlan0
dhcp-range=192.168.166.10,192.168.166.20,12h

.. note:: YMMV. If you use multiple SSID you might want to tweak the ``interface`` setting.

Reboot !
========

.. code-block:: bash

    sudo reboot

Griotte
=======

Installation
------------

.. code-block:: bash

    git clone https://github.com/erasme/griotte.git
    cd griotte
    make production

or if you need development libraries :

    make devel

Then, activate virtualenv :

    source bin/activate
    export PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH

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

    griotte/bin/adc
    griotte/bin/gpio
    griotte/bin/multimedia
    griotte/bin/director

Head to [the server](http://localhost:8888) (change localhost if you installed
it somewhere else), and start playing with the application !
