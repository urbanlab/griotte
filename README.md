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


# Getting started

    git clone ... griotte
    cd griotte

In the commands below, replace `python` by `python3` if python3 is not your
default python interpreter.

    python production-bootstrap.py
    python devel-bootstrap.py # if you need development libraries
    source bin/activate
    export PYTHONPATH=${PWD}/src/lib:$PYTHONPATH

You can then start the server with :

    src/bin/server

Head to [the server](http://localhost:8888) (change localhost if you installed
it somewhere else).

# Documentation

Documentation is in `docs/` in rst format. Il you installed development
dependencies, you can generate documentation by running :

    cd docs && make html





