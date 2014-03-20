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

import griotte.graceful

from griotte.multimedia.mediamanager import MediaManager

#from griotte.multimedia.fbi import Fbi
from griotte.multimedia.pgimage import PgImage
from griotte.ws import WebSocket

"""
Image handling class
"""

class ImageHandler:
    def __init__(self):
        self.backend = PgImage()
        self.ws = WebSocket(watchdog_interval=2)
        self.ws.add_listener('image.command.start', self.image_start)
        self.ws.add_listener('image.command.background', self.image_background)

        self.start()


    def image_background(self, channel, message):
        logging.debug("setting background to %s" % message['color'])
        self.backend.background(message['color'])
        self.send_status('start')
        self.ws.send("image.event.background", { "color": message['color']})

    def image_start(self, channel, message):
        # Message types :
        # play
        media = MediaManager.get_media_dict('image', message['media'])

        logging.debug("playing image %s" % media['path'])
        self.backend.play(media['path'])
        self.send_status('start')
        self.ws.send("image.event.start", { "media": self.backend.media })

    def start(self):
        logging.info("Starting ImageHandler's websocket")
        self.ws.start(detach=False)

