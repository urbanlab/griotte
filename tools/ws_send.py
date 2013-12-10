#!/usr/bin/env python3

import json
import sys

from websocket import create_connection

def send(channel, data):
  ws = create_connection("ws://localhost:8888/ws")

  decoded = json.loads(sys.argv[2])

  data = json.dumps( { 'channel': sys.argv[1], 'data': decoded } )
  print("In channel %s sending %s" % (sys.argv[1], data))
  ws.send(data)
  ws.close()

if __name__ == "__main__":
  if (len(sys.argv) != 3 or sys.argv[1] == "-h"):
    print("Usage: %s <channel> <json_data>" % sys.argv[0])
    exit(1)
  else:
    send(sys.argv[1],sys.argv[2])
