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
import signal

import griotte.graceful
from griotte.handler import Handler

from griotte.mediamanager import MediaManager
from griotte.image.pgimage import PgImage

"""
Image handling class
"""

class ImageHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

        self.backend = PgImage()
        self.add_listener('start')
        self.add_listener('background')

        self.start()

    def _signal(self, signum, frame):
        self.backend._shutdown()

    def _wscb_background(self, channel, message):
        logging.debug("setting background to %s" % message['color'])
        self.backend.background(message['color'])
        self.send_status('start', { "type": "background",
                                    "color": message['color']} )
        self.send_event("background", { "color": message['color']})

    def _wscb_start(self, channel, message):
        # Message types :
        # play
        media = MediaManager.get_media_dict('image', message['media'])

        logging.debug("Playing image %s" % media['path'])

        self.backend.play(media['path'])
        self.send_status('start', { "type" : "image",
                                    "media": message['media'] })
        self.send_event('start', { "media": self.backend.image })

    def start(self):
        logging.info("Starting ImageHandler's websocket")
        self._ws.start(detach=True)

    def send_status(self, status, message):
        logging.debug("sending status")
        self.send_event(status, message)

