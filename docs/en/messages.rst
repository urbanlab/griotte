********
Messages
********

Messages
========

A websocket message always consists of a channel name, a timestamp, and a data
part.

Channel names follow a dot-delimited hierarchical structure, that let the
clients use channel globbing subscription when required using '*'.

The data part is free form, and has a meaning for the clients only. The server
just handles pub/sub registration in the meta.* channel hierarchy, handles
message forwarding and doesn't care about other channels content. This let's you
implement your own channels if needed.

.. code-block:: json

    {
      "channel": "some.channel",
      "timestamp": 1389173038.4667788,
      "data" : { ... },
    }

The timestamp is in Python's time.time() format.

Current channel list and message definitions
============================================

* meta.subscribe
* meta.unsubscribe
* meta.join
* meta.leave

* store.get.<var>
* store.set.<var>
* store.push.<var>

Special vars : ``volume``, ``sound_mute``, ``videos``, ``audios``, ``images``

* <video|audio|image>.event.start
* <video|audio|image>.event.stop
* <video|audio|image>.event.status

* <video|audio|image>.command.start
* <video|audio|image>.command.stop
* <video|audio|image>.command.pause
* <video|audio|image>.command.rewind

* <analog|digital>.event.sample.<an[0-3]|io[0-3]>
* <analog|digital>.event.edge.<an[0-3]|io[0-3]>
* <analog|digital>.command.profile.<an[0-3]|io[0-3]>
* ``<analog|digital>.command.sample.<an[0-3]|io[0-3]>``

``mlqjkdfsdf``

meta
----

The meta namespace covers the pub/sub area.

meta.subscribe
^^^^^^^^^^^^^^

Sent by a client that want to subscribe to a channel.

.. code-block:: json

    {
      "channel": "meta.subscribe",
      "timestamp": <timestamp>,
      "data" : { "channel": "<channel.name>" },
    }

meta.unsubscribe
^^^^^^^^^^^^^^^^

Sent by a client that want to unsubscribe from a channel.

.. code-block:: json

    {
      "channel": "meta.unsubscribe",
      "timestamp": <timestamp>,
      "data" : { "channel": "<channel.name>" },
    }

meta.join
^^^^^^^^^

Broadcasted by the server to all clients when a new client joins. This message
is sent to all clients regardless if they are subscribed to the `meta.join`
channel or not.

.. code-block:: json

    "data": { "client": "<ip_address>:<client_port>" }

meta.leave
^^^^^^^^^^

Broadcasted by the server to all clients when a client leaves. This message
is sent to all clients regardless if they are subscribed to the `meta.leave`
channel or not.

.. code-block:: json

    "data": { "client": "<ip_address>:<client_port>" }

request
-------

This hierarchy typically contains messages sent to subsystems.

request.analog.<channel>
^^^^^^^^^^^^^^^^^^^^^^^^

Message sent to the analog handling subsystem. The channel must end with the analog port name of th RaspeOMix interface.
The port name value can be 'an0', 'an1', 'an2', 'an3'.

The data part contains a "type" key which can be one of the following :

get_value
"""""""""

Asks the sensor handler to send back a single sample message (not implemented).

periodic_sample
"""""""""""""""

Asks the sensor handler to send periodic samples. this message has the following
additional key :

* every : delay between sending a new sample message

set_profile
"""""""""""

Assigns a sensor profile to an analog port. The profile can have the following keys :

* name : a short profile name, typically representing the sensor's name (e.g.
  "Maxbotik EZ-1")
* description : a free form description of the profile
* units : what units this profile returns after conversion (free form)
* formula : a RPN formatted convertion formula to apply to the raw sensor value.
  See 'Formulas' below.
* valrange : sensor converted value range, used as floor/ceil values after
  convertion.
* resolution : RaspiOMix Analog/Digital converter resolution (default is '12bits';
  can be one of '12bits', '14bits', '16bits' or '18bits')
* gain : Analog/Digital converter gain (default is '1x', can be '1x', '2x', '4x' or '8x')

Griotte only supports RaspiOMix's MCP3424 ADC for now.

Example, assigning a thermistor-type profile to analog 0 port :

.. code-block:: json

    {
        "channel": "request.analog.an0",
        "timestamp": <timestamp>,
        "data":
        {
            "type": "set_profile",
            "name": "Grove Temperature Sensor",
            "units": "°C",
            "formula": "$x 5.06 / 1024 * dup 1023 swap - swap 10000 * swap / 10000 / log10 3975 / 298.15 inv + inv 273.15 -",
        }
    }

request.sound
^^^^^^^^^^^^^

Tells the sound player to either play, pause or stop the media.

.. code-block:: json

    "data": { "command": "[play|pause|stop]" }

request.video
^^^^^^^^^^^^^

Tells the video player to either play, pause or stop the media.

.. code-block:: json

    "data": { "command": "[play|pause|stop]" }

message
-------

message.video
^^^^^^^^^^^^^

Gratuitous


