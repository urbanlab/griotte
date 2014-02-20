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
# tools/ws_send.py request.video '{ "command": "play", "media": "/home/pi/kitten.mp4" }'

import logging
import json

import griotte.graceful

from time import sleep

from griotte.multimedia.omxplayer import OMXPlayer
from griotte.ws import WebSocket

"""

"""

class ImageHandler:
    def __init__(self):
        self.backend = Fbi()
        self.ws = WebSocket(watchdog_interval=2)
        self.ws.add_listener('image.command.start', self.image_request)

        self.start()


    def image_request(self, channel, message):
        # Message types :
        # play
        if channel == 'image.command.start':
            logging.debug("playing image %s" % message['media'])
            self.backend.play(message['media'])
            self.send_status('start')

    def send_status(self, status = "status"):
        logging.debug("sending status")
        message = { "media": self.backend.media }

        self.ws.send("video.event." + status, message)

    def start(self):
        logging.info("Starting ImageHandler's websocket")
        self.ws.start(detach=False)

