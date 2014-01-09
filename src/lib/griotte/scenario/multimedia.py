#
# (c) 2013-2014 ERASME
#
# This file is part of griotte
#
# griotte is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# griotte is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with griotte. If not, see <http://www.gnu.org/licenses/>.

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
    send('meta.store.sound_level.set',
         '{ "level":"%s" }' % int(level))

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
