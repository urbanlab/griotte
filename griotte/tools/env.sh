#!/bin/bash

echo -n "Activating virtualenv............................."
source bin/activate
echo "ok"
echo -n "Reading config from griotte/config/griotte.conf..."
source griotte/config/griotte.conf
echo "ok"
echo -n "Fixing path......................................."
export PYTHONPATH=/home/leucos/dev/raspberry/griotte/griotte/lib:$PYTHONPATH
echo "ok"

