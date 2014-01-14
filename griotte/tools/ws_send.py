#!/usr/bin/env python3

# Examples :
# python tools/ws_send.py request.analog.an1 '{ "type": "periodic_sample", "every": 5}'
# python tools/ws_send.py request.analog.an1 '{ "type": "set_profile", "profile": { "name": "Grove Temp", "formula": "$x 5.06 / 1024 * dup 1023 swap - swap 10000 * swap / 10000 / log10 3975 / 298.15 inv + inv 273.15 -" }}'


import json
import sys

from time import time

from websocket import create_connection

def send(channel, data):
  ws = create_connection("ws://localhost:8888/ws")

  decoded = json.loads(sys.argv[2])

  data = json.dumps( { 'channel': sys.argv[1], 'timestamp': time(), 'data': decoded } )
  print("In channel %s sending %s" % (sys.argv[1], data))
  ws.send(data)
  ws.close()

if __name__ == "__main__":
  if (len(sys.argv) != 3 or sys.argv[1] == "-h"):
    print("Usage: %s <channel> <json_data>" % sys.argv[0])
    exit(1)
  else:
    send(sys.argv[1],sys.argv[2])
