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

# Original code from https://github.com/jbaiter/pyomxplayer

import threading
import pexpect
import re
import logging
from threading import Thread
from time import sleep

import sys

class OMXPlayer(object):

    #_FILEPROP_REXP = re.compile(r".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(b"Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+)")
    _AUDIOPROP_REXP = re.compile(b"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _SUBTITLES_REXP = re.compile(b"Subtitle count: (\d+), state: (\w+), index: (\d+), delay: (\d+)")
    _STATUS_REXP = re.compile(b".*duration:(\d+),pos:(\d+),state:(\d+),volume:([-]?\d+),amplitude:(\d+),muted:(\d+)")
    _WILDCARD_REXP = re.compile(b"(.*)")

    #duration:11005,pos:276,state:1,volume:0,amplitude:100,muted:0

    #_STATUS_REXP = re.compile(r"duration:(.*),")
    _DONE_REXP = re.compile(b"have a nice day.*")

    _LAUNCH_CMD = '/usr/bin/omxplayer --vol %s %s'

    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _TOGGLE_MUTE_CMD = '*'
    _INFO_CMD = '?'
    _QUIT_CMD = 'q'


    # def percent_to_millibels(x):
    #     # Cubic fit from {0,-6000}, {10,-4605}, {20,-3218},{30,-2407},{40,-1832},{50,-1386},{60,-1021},{70,-713},{80,-446},{90,-210},{100,0},{110,190},{120,364}
    #     return 0.00603904*x**3-1.59426*x**2+157.732*x-5956.12

    def percent_to_millibels(x):
        # Converts a percentage to a specific OMXPlayer command
        if x<=0:       return -6000
        if 0<x<=10:    return -4605
        if 10<x<=20:   return -3218
        if 20<x<=30:   return -2407
        if 30<x<=40:   return -1832
        if 40<x<=50:   return -1386
        if 50<x<=60:   return -1021
        if 60<x<=70:   return  -713
        if 70<x<=80:   return  -446
        if 80<x<=90:   return  -210
        if 90<x<=100:  return     0
        if 100<x<=110: return   190
        return 364

    def percent_to_command(x):
        # Converts a percentage to a specific OMXPlayer command
        if x<=0:       return 'A'
        if 0<x<=10:    return 'B'
        if 10<x<=20:   return 'C'
        if 20<x<=30:   return 'D'
        if 30<x<=40:   return 'E'
        if 40<x<=50:   return 'F'
        if 50<x<=60:   return 'G'
        if 60<x<=70:   return 'H'
        if 70<x<=80:   return 'I'
        if 80<x<=90:   return 'J'
        if 90<x<=100:  return 'K'
        if 100<x<=110: return 'L'
        return 'M'

    def millibels_to_percent(x):
        # Quadratic fit from {-6000,0},{-4605,10},{-3218,20},{-2407,30},{-1832,40},{-1386,50},{-1021,60},{-713,70},{-446,80},{-210,90},{0,100},{190,110},{364,120} doesn't work
        #return 3.77886*10**-6*x**2+0.0383572*x+99.3722

        if x <= -6000: return   0
        if x <= -4605: return  10
        if x <= -3218: return  20
        if x <= -2407: return  30
        if x <= -1832: return  40
        if x <= -1386: return  50
        if x <= -1021: return  60
        if x <=  -713: return  70
        if x <=  -446: return  80
        if x <=  -210: return  90
        if x <=     0: return 100
        if x <=   190: return 110
        return 120

    def __init__(self, status_callback):
        self._position_thread = None
        self._process = None
        self._status_callback = status_callback
        self.subtitles_visible = False

        # Initialize status variables
        self.muted = False
        self.volume = self.amplitude = 0

    def play(self, mediafile, subtitles=False):
        self.playing = False
        self.position = self.media_length = 0
        self.media = mediafile

        cmd = self._LAUNCH_CMD % (self.volume, mediafile)

        logging.debug("launchcmd : %s" % cmd)
        self._process = pexpect.spawn(cmd)
        fout = open('mylog.txt','bw')
        self._process.logfile = fout

        self.video = dict()
        self.audio = dict()
        self.subtitles = dict()

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
        # Get subtitles properties
        subtitles_props = self._SUBTITLES_REXP.match(self._process.readline()).groups()
        self.subtitles['count'] = audio_props[0]
        self.subtitles['state'] = audio_props[1]
        self.subtitles['index'] = audio_props[2]
        self.subtitles['delay'] = audio_props[3]

        self._position_thread = threading.Thread(target=self._get_position, args=())
        self._position_thread.daemon = True
        self._position_thread.start()

        if subtitles:
            self.toggle_subtitles()

    def _get_position(self):
        while True:
            self._process.send(self._INFO_CMD)
            index = self._process.expect_list([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP],
                                            timeout=1)

            logging.debug("expect returned position: %s" % index)

            if index == 1: continue
            elif index in (2, 3): break
            elif index == 0:
                matches = self._process.match.groups()
                self.position = float(matches[1])
                self.media_length = float(matches[0])
                self.playing = True if matches[2].decode('ascii') == "1" else False
                self.volume = OMXPlayer.millibels_to_percent(int(matches[3]))
                self.amplitude = int(matches[4])
                self.muted = True if matches[5].decode('ascii') == "1" else False

                logging.debug("position: %s, playing: %s, volume: %s" %
                              (self.position, self.playing, self.volume))
                self._status_callback('status')
            sleep(0.1)
        logging.debug("ending _get_position thread")
        self.stop()

    def toggle_pause(self):
        logging.warning("sending _PAUSE_CMD")
        if self._process.send(self._PAUSE_CMD):
            self.playing = not self.playing

        if self.playing:
            self._status_callback('resume')
        else:
            self._status_callback('pause')

    def mute(self, sound="toggle"):
        logging.debug("received call to mute with state %s" % sound)
        if sound == "toggle":
            self._toggle_mute()
        elif sound == 'off' and not self.muted:
            self._toggle_mute()
        elif sound == 'on' and self.muted:
            self._toggle_mute()

    def _toggle_mute(self):
        logging.debug("sending mute command %s" % self._TOGGLE_MUTE_CMD)
        if self._process.send(self._TOGGLE_MUTE_CMD):
            self.muted = not self.muted

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible
            self._status_callback('toggle_subtitles')

    def is_running(self):
        return self._position_thread.is_alive() or self._process.isalive()

    def is_playing(self):
        return self._process and self.playing and self.is_running()

    def stop(self):
        logging.debug("stopping omxplayer")
        self._process.send(self._QUIT_CMD)
        self._process.close(force=True)
        self._status_callback('stop')

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        # Nothing to do if we're muted
        # this is important : omxplayer will reset muting state if volume changes
        # when mute is off
        logging.debug("received volume command - state before change is level=%s, muted=%s" % (self.volume,self.muted))

        self.volume = OMXPlayer.percent_to_millibels(int(volume))
        if self.muted: return

        if self.is_playing():
            logging.debug("sending volume command %s" % OMXPlayer.percent_to_command(volume))
            if self._process.send(OMXPlayer.percent_to_command(volume)):
                self._status_callback('changed_volume')

    def seek(self, minutes):
        raise NotImplementedError
