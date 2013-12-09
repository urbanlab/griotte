#
# (c) 2013 ERASME
#
# This file is part of Raspeomix
#
# Raspeomix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Raspeomix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import json
import socket
import time

try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.

import websocket

class WebSocket:
    """ WebSocket client """

    prefix = ""

    def __init__(self, channel, callback):
        self.prefix = socket.gethostname()
        self.callback = callback
        self.channel = channel
        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp("ws://127.0.0.1:8888/ws",
                            on_message = self.on_message,
                            on_error = self.on_error,
                            on_close = self.on_close)

        self.ws.on_open = self.on_open
        thread.start_new_thread(self.start, ())

    def start(self):
        print("starting ws")
        self.ws.run_forever()
        print("forever ?")

    def on_message(self, ws, message):
        print("received : %s" % message)
        self.callback(message)

    def on_error(self):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(self, ws):
        print("### opened ###")
        data = json.dumps( { 'channel': '/meta/register',
                            'data': { 'channel': self.channel } } )


    def debug(self):
        print ("hello %s",__main__)

if __name__ == "__main__":
    def func(message):
        print("in callback with %s" % message)
    ws = WebSocket('an',func)

    time.sleep(100)
