Installation, the easy way
**************************

Installation from premade image for the lazy and the impatient.

Image & base config
===================

* Download Griotte image from http://griotte.erasme.org/downloads/
* Uncompress with

.. code-block:: bash

    unzip griotte-0.0.9.img.zip

* Dump to SD card

.. code-block:: bash

    sudo dcfldd if=griotte-0.0.9.img of=/dev/sdc bs=1m sizeprobe=if status=on
    sync

.. note:: If you don't have ``dfcldd``, the classic alternative ``sudo dd if=griotte-0.0.9.img of=/dev/sdc bs=1m && sync`` will work.

* Plug a supported Wireless dongle in your Raspberry (or use Ethernet if you prefer)
* Boot !
* Join the wireless network `griotte` (open)
* Head your browser to http://192.168.3.1:8888/admin/

