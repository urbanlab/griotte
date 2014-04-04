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
from griotte.handler import Handler
from griotte.multimedia.mediamanager import MediaManager

#from griotte.multimedia.fbi import Fbi
from griotte.multimedia.pgimage import PgImage
from griotte.ws import WebSocket

"""
Image handling class
"""

class ImageHandler(Handler):
    def __init__(self):
        Handler.__init__(self, 'image')

        self.backend = PgImage()
        self._ws.add_listener('image.command.start', self.image_start)
        self._ws.add_listener('image.command.background', self.image_background)
        self._ws.add_listener('image.command.ping', self.image_start)

        self.start()

    def image_background(self, channel, message):
        logging.debug("setting background to %s" % message['color'])
        self.backend.background(message['color'])
        self.send_status('start', { "type": "background",
                                    "color": message['color']} )
        self._ws.send("image.event.background", { "color": message['color']})

    def image_start(self, channel, message):
        # Message types :
        # play
        media = MediaManager.get_media_dict('image', message['media'])

        logging.debug("Playing image %s" % media['path'])

        self.backend.play(media['path'])
        self.send_status('start', { "type" : "image",
                                    "media": message['media'] })
        self._ws.send("image.event.start", { "media": self.backend.media })

    def start(self):
        logging.info("Starting ImageHandler's websocket")
        self._ws.start(detach=False)


    def send_status(self, status, message):
        logging.debug("sending status")

        self._ws.send("image.event." + status, message)

