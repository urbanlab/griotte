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
from griotte.multimedia.mediamanager import MediaManager

from griotte.ws import WebSocket

"""

"""

class MultimediaHandler:
    def __init__(self):
        self.backend = OMXPlayer(self.send_status)
        self.ws = WebSocket(watchdog_interval=2)
        self.ws.add_listener('video.command.*', self.video_request)
        self.ws.add_listener('store.command.set.sound_level', self.sound_level)

        self.start()

    def sound_level(self, channel, message):
        # toggle_mute
        # unmute
        # mute
        # set_volume
        if 'level' in message['value']:
            self.backend.set_volume(message['value']['level'])
        if 'state' in message['value']:
            self.backend.mute(message['value']['state'])

    def video_request(self, channel, message):
        # Message types :
        # toggle_pause
        # play
        # stop
        media = MediaManager.get_media_dict('video', message['media'])

        from pprint import pprint
        pprint(media)

        if channel == 'video.command.pause':
            logging.debug("pausing media")
            self.backend.toggle_pause()
            #self.send_status('toggle_pause') => send by cb
        elif channel == 'video.command.start':
            logging.debug("playing media %s" % media['path'])
            self.backend.play(media['path'])
            self.send_status('start')
        elif channel == 'video.command.stop':
            logging.debug("stopping current media")
            self.backend.stop()
            #self.send_status('stop')

    def send_status(self, status = "status"):
        logging.debug("sending status")
        message = { "position": self.backend.position,
                    "duration": self.backend.media_length,
                    "playing": self.backend.playing,
                    "volume": self.backend.volume,
                    "amplitude": self.backend.amplitude,
                    "muted": self.backend.muted,
                    "media": self.backend.media }

        self.ws.send("video.event." + status, message)

    def start(self):
        logging.info("Starting MultimediaHandler's websocket")
        self.ws.start(detach=False)

