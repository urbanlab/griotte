Messages
********

Overview
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

meta
----

The meta namespace covers the pub/sub area. It is mainly used by
Javascript/Python pub/sub implementation.

* meta.subscribe
* meta.unsubscribe
* meta.join
* meta.leave

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

multimedia events
-----------------

Event messages are emited by various subsystems to indicate that some condition
or event occured.
They can be emitted for video, audio and image playback.

<video|audio|image>.event.start
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sent when a video, a sound or an image is starts playing.

<video|audio|image>.event.stop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sent when a video, a sound or an image playback is stopped. Stopped means that
the player is not able to resume playback.

<video|audio|image>.event.pause
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sent when a video, a sound or an image playback is paused. A paused media can be
resumed with `<video|audio|image>.command.resume`_ .

<video|audio|image>.event.resume
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sent when a media is resumed with `<video|audio|image>.command.resume`_ after a
pause.

<video|audio|image>.event.status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Send periodically by media players during playback.
Status event data may containt the following fields:

* **position** : the current position in the media, in msecs
* **duration** : the total duration of the media
* **playing** : the current playback state (True if playing, false if paused)
* **volume** : the playback volume in percent (0-120%)
* **amplitude** : the playback amplitude (not used ATM)
* **muted** : whether the media is currently muted
* **media** : the media name in the storage

<video|audio|image>.event.changed_volume
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Triggered when the volume is changed

.. note:: This will be deprecated

hardware events
---------------

<an[0-3]|io[0-3]>.event.sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Events sent from the analog and digital handling subsystem. The port must end
with the analog or digital port name of th RaspeOMix interface. The port name
value can be 'an0', 'an1', 'an2', 'an3', 'io0', io', 'io2', 'io3'.

An analog sample always return the current port profile (name, description,
units, formula, range, resolution, gain), the raw_value and the converted
value.

* **name** : profile name
* **description** : profile description
* **units** : measurement units after conversion
* **formula** : conversion RPN formula
* **range** : value range
* **resolution** : ADC sampling resolution
* **gain** : ADC gain
* **raw_value** : raw value in mV
* **converted_value** : value after converion (in units specified in the profile)

<an[0-3]|io[0-3]>.event.edge.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: TBD

multimedia commands
-------------------

Commands are typically send between clients to play medias or configure some
apstecs of the system.

<video|audio|image>.command.start
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Loads and play a media immediately.
The message contains the following field :

* **media** : the media name in the media storage

A `<video|audio|image>.event.start`_ event is emitted in response to a stop
command, and the player might send several `<video|audio|image>.event.status`_
events during the playback.

<video|audio|image>.command.stop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops media playback completely. The media can not be resumed after a stop
command. A `<video|audio|image>.event.stop`_ event is emitted in response to a
stop command.

<video|audio|image>.command.pause
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pauses media playback A `<video|audio|image>.event.pause`_ event is emitted in
response to a pause command. A paused media can be resumed with
`<video|audio|image>.command.resume`_ .

<video|audio|image>.command.resume
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Resumes a previously paused media. A `<video|audio|image>.event.resume`_ event
is emitted in response to a resume command.

<video|audio|image>.command.rewind
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Restarts media playback from the beginning. No specific event is emitted after a
resume command.

analog/digital converted commands
---------------------------------

Messages sent to the analog handling subsystem. The port must end with the
analog port name of th RaspeOMix interface. The port name value can be 'an0',
'an1', 'an2', 'an3'.

analog.command.<port>.sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Asks the sensor handler to send back a single sample message (not implemented).

analog.command.<port>.periodic_sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Asks the sensor handler to send periodic samples. this message has the following
data field  :

* **every** : delay between sending a new sample message

analog.command.<port>.profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assigns a sensor profile to analog port <port>. The profile can have the
following keys :

* **name** : a short profile name, typically representing the sensor's name (e.g.
  "Maxbotik EZ-1")
* **description** : a free form description of the profile
* **units** : what units this profile returns after conversion (free form)
* **formula** : a RPN formatted convertion formula to apply to the raw sensor value.
  See 'Formulas' below.
* **valrange** : sensor converted value range, used as floor/ceil values after
  convertion.
* **resolution** : RaspiOMix Analog/Digital converter resolution (default is '12bits';
  can be one of '12bits', '14bits', '16bits' or '18bits')
* **gain** : Analog/Digital converter gain (default is '1x', can be '1x', '2x', '4x' or '8x')

Griotte only supports RaspiOMix's MCP3424 ADC for now.

Example, assigning a thermistor-type profile to analog 0 port :

.. code-block:: json

    {
        "channel": "analog.command.an0.profile",
        "timestamp": <timestamp>,
        "data":
        {
            "name": "Grove Temperature Sensor",
            "description": "Themistor temperature sensor. See datasheet at http://garden.seeedstudio.com/index.php?title=GROVE_-_Starter_Bundle_V1.0b#Temperature_Sensor_Twig"
            "units": "°C",
            "formula": "$x 5.06 / 1024 * dup 1023 swap - swap 10000 * swap / 10000 / log10 3975 / 298.15 inv + inv 273.15 -",
        }
    }


storage commands
----------------

Special vars : ``volume``, ``sound_volume``, ``videos``, ``audios``, ``images``

store.get.<var>
^^^^^^^^^^^^^^^

.. note:: TBD

store.set.<var>
^^^^^^^^^^^^^^^

.. note:: TBD

store.push.<var>
^^^^^^^^^^^^^^^^

.. note:: TBD







* <analog|digital>.command.profile.<an[0-3]|io[0-3]>
* ``<analog|digital>.command.sample.<an[0-3]|io[0-3]>``

``mlqjkdfsdf``
