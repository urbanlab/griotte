#!/bin/sh

export PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH
export LOGGING=${1:-INFO}

tmux new-session -d -s griotte -n Griotte /bin/bash
tmux new-window -t griotte:1 -n Server "griotte/bin/server --logging=$LOGGING; /bin/bash"

sleep 3

tmux new-window -t griotte:2 -n Storage "griotte/bin/storage --logging=$LOGGING; /bin/bash"
tmux new-window -t griotte:3 -n Multimedia "griotte/bin/multimedia --logging=$LOGGING; /bin/bash"

if [ -n "$SSH_CONNECTION" ]; then
  # We're running from ssh - we need sudo :()
  tmux new-window -t griotte:4 -n Image "sudo PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH DISPLAY= griotte/bin/image --logging=$LOGGING; /bin/bash"
else
  tmux new-window -t griotte:4 -n Image "griotte/bin/image --logging=$LOGGING; /bin/bash"
fi

tmux new-window -t griotte:5 -n ADC "griotte/bin/adc --logging=$LOGGING; /bin/bash"
tmux new-window -t griotte:6 -n GPIO "sudo PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH griotte/bin/gpio --logging=$LOGGING; /bin/bash"

tmux new-window -t griotte:7 -n GPIO "sudo PYTHONPATH=${PWD}/griotte/lib:$PYTHONPATH griotte/bin/rfid --logging=$LOGGING; /bin/bash"

tmux select-window -t griotte:1
tmux attach-session -d -t griotte
