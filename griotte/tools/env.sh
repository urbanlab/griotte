#!/bin/bash

echo -n "Activating virtualenv............................."
source bin/activate
echo "ok"
echo -n "Fixing path......................................."
export PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH
echo "ok"

