#!/usr/bin/env python3

import json
import sys

import websocket

def on_open(ws):
  ws.send('{ "channel":"/meta/subscribe","data":{"channel":"%s"}}' % sys.argv[1])

def on_message(ws, message):
  print(message)

def on_error(ws, error):
  print(error)

def on_close(ws):
  print("### closed ###")

def listen():
  ws = websocket.WebSocketApp("ws://localhost:8888/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
  ws.on_open = on_open
  ws.run_forever()

if __name__ == "__main__":
  if (len(sys.argv) != 2 or sys.argv[1] == "-h"):
    print("Usage: %s <channel>" % sys.argv[0])
    exit(1)
  else:
    listen()
