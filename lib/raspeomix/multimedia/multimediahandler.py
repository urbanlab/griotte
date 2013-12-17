#
# (c) 2013-2014 ERASME
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
# along with Raspeomix. If not, see <http://www.gnu.org/licenses/>.


from raspeomix.multimedia.omxplayer import OMXPlayer
from raspeomix.ws import WebSocket
from time import sleep

import logging
import json

"""
Messages:

request:video { "status???" }
request:video { "command": "pause" }

message:video { "status" : "playing", "time" : 12 ... }

All exchanged messages have a timestamp

"""

class MultimediaHandler:
    def __init__(self):
        self.backend = OMXPlayer()
        self.ws = WebSocket(watchdog_interval=2)
        self.ws.add_listener('request.video', self.request)

        self.start()

    def request(self, channel, message):
        # Message types :
        # toggle_pause
        # play
        # stop
        # toggle_mute
        # unmute
        # mute
        logging.info("got request")

        if message['command'] == 'toggle_mute':
            logging.debug("toggling mute")
            self.backend.toggle_mute()
            self.send_status()
        elif message['command'] == 'pause':
            logging.debug("pausing media")
            self.backend.toggle_pause()
            self.send_status()
        elif message['command'] == 'play':
            logging.debug("playing media %s" % message['media'])
            self.backend.play(message['media'])
            self.send_status()

    def send_status(self):
        logging.debug("sending status")
        status = {  "type" : "status",
                    "position": self.backend.position,
                    "media_length": self.backend.media_length,
                    "state": self.backend.state,
                    "volume": self.backend.volume,
                    "amplitude": self.backend.amplitude,
                    "muted": self.backend.muted }
        self.ws.send("message.video", status)

    def start(self):
        logging.info("Starting MultimediaHandler's websocket")
        self.ws.start()
        sleep(100)

if __name__ == "__main__":
    import tornado.options
    tornado.options.parse_command_line()

    MultimediaHandler()
