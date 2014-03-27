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

# Example:
# tools/ws_send.py dmx.command.send '{ "channels" => { "1" => 127, "3" => 12 } }'

import logging

import griotte.graceful

#from griotte.multimedia.fbi import Fbi
from griotte.dmx.enttec import Enttec
from griotte.ws import WebSocket

"""
DMX handling class
"""

class DMXHandler:
    def __init__(self):
        self.backend = Enttec()
        self.ws = WebSocket(watchdog_interval=2)
        self.ws.add_listener('dmx.command.send', self.send)
        self.ws.add_listener('dmx.command.clear', self.send)

        self.start()

    def send(self, channel, message):
        self.backend.set_channels(message['channels'])

    def clear(self, channel, message):
        # logging.debug("setting background to %s" % message['color'])
        # self.backend.background(message['color'])
        # self.send_status('start', { "type": "background",
        #                             "color": message['color']} )
        # self.ws.send("image.event.background", { "color": message['color']})
        self.backend.clear_channels(message['channels'])

    def start(self):
        logging.info("Starting DMXHandler's websocket")
        self.ws.start(detach=False)
