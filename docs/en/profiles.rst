********
Profiles
********

Profiles are used to configure sensors subsystems. These subsystems listen to
specific channels (see :doc:`messages`) for profile configuration :

* analog : analog.command.<port>.profile
* digital : digital.command.<port>.profile

They are sent over websockets to configure several subsystem's aspects.

Analog sensors
==============

Analog sensors support the following fields in the profile :

+-------------+------------------------------------------------------------------+----------------------+
| Field       | Purpose                                                          | Valid values         |
+=============+==================================================================+======================+
| name        | name of the profile                                              | free form            |
+-------------+------------------------------------------------------------------+----------------------+
| description | human readable short description of the profile                  | free form            |
+-------------+------------------------------------------------------------------+----------------------+
| units       | units for the data returned by the profile after conversion      | free form            |
+-------------+------------------------------------------------------------------+----------------------+
| formula     | formula used to covert the raw sensor voltage to values in units | see `Formulas`_      |
+-------------+------------------------------------------------------------------+----------------------+
| range       | range of values returned by the raw sensor                       | not used             |
+-------------+------------------------------------------------------------------+----------------------+
| resolution  | resolution required to sample the sensor                         | `Devices`_ dependent |
+-------------+------------------------------------------------------------------+----------------------+
| gain        | amplification gain to apply to the sample                        | `Devices`_ dependent |
+-------------+------------------------------------------------------------------+----------------------+

If not profile is attributed to the port, the 'Identity' profile will be used
(12bits sampling, 1x gain, not unit, no conversion) : you just get the raw
voltage.

Devices
-------

The analog subsystem has been written to support multiple analog/device
converters (ADC).

MCP342x
^^^^^^^

The MCP342x chip the the only implemented at the moment. This chip is used by
the RaspiOMix daughter card.

This chip supports the following resolutions : '12bits', '14bits', '16bits',
'18bits'. The higher the resolution, the lower the sampling rate will be. Thus,
using sampling rates instead of precision yields the same results. In the same
order, the sampling rates are : '240sps', '60sps', '15sps', '3_75sps'.

It provides the following analog ports : ``an0``, ``an1``, ``an2``, ``an3``.

The RaspiOMix card additionnaly provides the following digital ports : ``io0``,
``io1``, ``io2``, ``io3``, ``dip0``, ``dip1``.

Formulas
--------

Profile formulas are expressed in RPN notation. The sensor raw value can be accessed with '$x'.

For instance, if you wan to write a profile that just doubles the value of the
sensor and gets it's square root, the formula would be :

    $x 2 * sqrt

Stack operations
^^^^^^^^^^^^^^^^

- ``drop`` : drops the last item on the stack
- ``dup``  : duplicates the last item of the stack
- ``swap`` : swaps the last item and the previous item on the stack

Math constants
^^^^^^^^^^^^^^

- ``pi`` : somewhere around 3.14
- ``e``  : base of natural logarithms

Math operations
^^^^^^^^^^^^^^^

Most of math operations are supported, including boolean ones. Check
:mod:`griotte.rpncalc`. for a complete and up to date list.

Digital sensors
===============

Profiles for digital sensors contains a bit less information than their analog friends :

+--------------+-----------------------------------------------------+-----------------------------------------+
| Field        | Purpose                                             | Valid values                            |
+==============+=====================================================+=========================================+
| name         | name of the profile                                 | free form                               |
+--------------+-----------------------------------------------------+-----------------------------------------+
| description  | human readable short description of the profile     | free form                               |
+--------------+-----------------------------------------------------+-----------------------------------------+
| debounce     | debounce timeout for the port                       | typically between 10 and 100 (ms)       |
+--------------+-----------------------------------------------------+-----------------------------------------+
| invert       | whether the handler will invert the sensor readings | for sensors with inverted logic         |
+--------------+-----------------------------------------------------+-----------------------------------------+
| direction    | whether the pin is input or output                  | inout for sensors, output for actuators |
+--------------+-----------------------------------------------------+-----------------------------------------+
| pull_up_down | whether to activate pull up or down on the port     | 'up', 'down', 'off' (default)           |
+--------------+-----------------------------------------------------+-----------------------------------------+
| invert       | whether the handler will invert the sensor readings | for sensors with inverted logic         |
+--------------+-----------------------------------------------------+-----------------------------------------+


