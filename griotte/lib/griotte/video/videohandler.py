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
from griotte.handler import Handler

from time import sleep

from griotte.video.omxplayer import OMXPlayer
from griotte.mediamanager import MediaManager

"""

"""

class VideoHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

        self.backend = OMXPlayer(self.send_status)

        #self.add_listener('pause', callback=self._wscb_video_request)
        self.add_listener('pause')
        self.add_listener('start')
        self.add_listener('stop')
        self.add_listener('storage.command.set.sound_level', full_path=True)

        self.start()

    def _wscb_sound_level(self, channel, message):
        # toggle_mute
        # unmute
        # mute
        # set_volume
        if 'level' in message['value']:
            self.backend.set_volume(message['value']['level'])
        if 'state' in message['value']:
            self.backend.mute(message['value']['state'])

    def _wscb_pause(self, channel, message):
        logging.debug("pausing media")
        self.backend.toggle_pause()

    def _wscb_start(self, channel, message):
        media = MediaManager.get_media_dict('video', message['media'])

        logging.debug("playing media %s" % media['path'])
        self.backend.play(media['path'])
        self.send_status('start')

    def _wscb_stop(self, channel, message):
            logging.debug("stopping current media")
            self.backend.stop()

    def send_status(self, status = "status"):
        logging.debug("sending status")
        message = { "position": self.backend.position,
                    "duration": self.backend.media_length,
                    "playing": self.backend.playing,
                    "volume": self.backend.volume,
                    "amplitude": self.backend.amplitude,
                    "muted": self.backend.muted,
                    "media": self.backend.media }

        self.send_event(status, message)

    def start(self):
        logging.info("Starting MultimediaHandler's websocket")
        self._ws.start(detach=False)

