Griotte
=======

Griotte is a framework that turns a Raspberry Pi into a programmable multimedia
player.

Associated with a [RaspiOMix](https://github.com/hugokernel/RaspiOMix) interface
and sensors (temperature, distance, RFID, ..., you name it), the player can
react to external events, activate external devices, drive lights via DMX, ...

While RaspiOMix uses [SeeedStudio's Grove
system](http://www.seeedstudio.com/wiki/GROVE_System), giving access to a wide
range of sensors and actuators, any 3.3v/5v sensor can be used.

Griotte can play scenarios written with
[Blockly](https://code.google.com/p/blockly/) simply by dragging and dropping
blocks.

Applications include museum players (that can react to visitors for instance),
educational tools (learning about programming or sensors), home automation,
lighting systems, ...

# Requirements

You need :
- a Raspberry Pi (but you can run/develop non-hardware related anywhere)
- python3
- pip
- virtualenv

On a Raspbian :

    sudo apt-get install python3-pip python-virtualenv

should be enough to install all dependencies.

# Getting started

    git clone https://github.com/erasme/griotte.git
    cd griotte
    make production

or if you need development libraries :

    make devel

Then, activate virtualenv :

    source bin/activate
    export PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH

You might need to adjust your python3 path in the top-level Makefile.

You can then start the server with :

    griotte/bin/server

Head to [the server](http://localhost:8888) (change localhost if you installed
it somewhere else).

Now to make something "real", please head to the
[documentation](http://griotte.erasme.org/docs/).

# Documentation

Documentation is in `docs/` in rst format. If you installed development
dependencies, you can generate documentation by running :

    make docs

Then `make rtfm` to read the docs,






