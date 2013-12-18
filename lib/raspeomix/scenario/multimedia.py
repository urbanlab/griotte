import json
import sys
import time

from websocket import create_connection

def play_video(media):
    ws = send('request.video',
              '{ "command": "play", "media": "' + media + '" }',
              close=False)
    expect(ws, 'message.video', type='stop')

def play_sound(media):
    ws = send('request.video',
              '{ "command": "play", "media": "' + media + '" }',
              close=False)
    expect(ws, 'message.video', type='stop')

def set_volume(level):
    send('meta.store.sound_level',
         "{ \"level\":\"%s\" }" % int(level))

def send(channel, data, close=True, ws=None):
    # Open websocket if we're not given one
    if ws == None:
        ws = create_connection("ws://localhost:8888/ws")

    print(data)
    decoded = json.loads(data)

    data = json.dumps( { 'channel': channel, 'data': decoded } )
    print("In channel %s sending %s" % (channel, data))
    ws.send(data)
    if close: ws.close()

    return ws

def expect(ws, channel, type=None):
    data = json.dumps( { 'channel': 'meta.subscribe',
                         'timestamp': time.time(),
                         'data': { 'channel': channel } } )
    ws.send(data)

    found = False
    while not found:
        message = ws.recv()
        decoded = json.loads(message)
        if decoded['channel'] == channel and decoded['data']['type'] == type:
            found = True;
