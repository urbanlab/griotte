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

# Original code from https://github.com/jbaiter/pyomxplayer

import threading
import pexpect
import re
import logging

from threading import Thread
from time import sleep

class OMXPlayer(object):

    #_FILEPROP_REXP = re.compile(b".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(b".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(b"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP = re.compile(b"duration:(\d+),pos:(\d+),state:(\d+),volume:(\d+),amplitude:(\d+),muted:(\d+)")

    #duration:11005,pos:276,state:1,volume:0,amplitude:100,muted:0

    #_STATUS_REXP = re.compile(b"duration:(.*),")
    _DONE_REXP = re.compile(b"have a nice day.*")

    _LAUNCH_CMD = '/home/pi/omxplayer %s'

    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _TOGGLE_MUTE_CMD = '*'
    _INFO_CMD = '?'
    _QUIT_CMD = 'q'

    def __init__(self):
        self._position_thread = None

    def play(self, mediafile, subtitles=False):
        self.subtitles_visible = False

        # Initialize status variables
        self.position = self.media_length = 0
        self.playing = self.muted = False
        self.volume = self.amplitude = 0

        cmd = self._LAUNCH_CMD % (mediafile)

        if self._position_thread is not None and self._position_thread.is_alive():
            self.stop()
            self._position_thread.join(0.5)

        logging.debug("launchcmd : %s" % cmd)
        #self._process = pexpect.spawn('/bin/bash', ['-c', cmd])
        self._process = pexpect.spawn(cmd)

        self.video = dict()
        self.audio = dict()

        # Get video properties
        video_props = self._VIDEOPROP_REXP.match(self._process.readline()).groups()
        self.video['decoder'] = video_props[0]
        self.video['dimensions'] = tuple(int(x) for x in video_props[1:3])
        self.video['profile'] = int(video_props[3])
        self.video['fps'] = float(video_props[4])
        # Get audio properties
        audio_props = self._AUDIOPROP_REXP.match(self._process.readline()).groups()
        self.audio['decoder'] = audio_props[0]
        (self.audio['channels'], self.audio['rate'],
        self.audio['bps']) = [int(x) for x in audio_props[1:]]

        self._position_thread = threading.Thread(target=self._get_position, args=())
        #self._position_thread = Thread(target=self._get_position)
        self._position_thread.daemon = True
        self._position_thread.start()

        if subtitles:
            self.toggle_subtitles()

    def _get_position(self):
        while True:
            self._process.send(self._INFO_CMD)
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP],
                                            timeout=1)

            if index == 1: continue
            elif index in (2, 3): break
            else:
                self.position = float(self._process.match.group(2))
                self.media_length = float(self._process.match.group(1))
                self.playing = True if self._process.match.group(3).decode('ascii') == "1" else False
                self.volume = int(self._process.match.group(4))
                self.amplitude = int(self._process.match.group(5))
                self.muted = True if self._process.match.group(6).decode('ascii') == "1" else False

                logging.debug("position: %s, playing: %s, volume: %s" %
                              (self.position, self.playing, self.volume))
            sleep(0.1)
        logging.debug("ending _get_position thread")

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            logging.warning("sending _PAUSE_CMD")
            self.playing = not self.playing

    def toggle_mute(self):
        if self._process.send(self._MUTE_CMD):
            self.muted = not self.muted

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible

    def is_running(self):
        return self._position_thread.is_alive() or self._process.isalive()

    def is_playing(self):
        return not self.playing and self.is_running()

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError
