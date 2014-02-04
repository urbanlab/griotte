#!/bin/sh

export PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH

tmux new-session -d -s griotte -n Griotte /bin/bash
tmux new-window -t griotte:1 -n Server griotte/bin/server

sleep 3

tmux new-window -t griotte:2 -n Storage griotte/bin/storage
tmux new-window -t griotte:3 -n Multimedia 'griotte/bin/multimedia; bash'
tmux new-window -t griotte:4 -n ADC griotte/bin/adc
tmux new-window -t griotte:5 -n GPIO 'sudo PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH griotte/bin/gpio'

tmux select-window -t griotte:1
tmux attach-session -d -t griotte
