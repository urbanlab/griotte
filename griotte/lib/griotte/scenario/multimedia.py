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

"""Server-side Multimedia groups blocks implementation

This module implements server-side code generated for multimedia blockly blocks.

.. module:: multimedia
   :platform: Unix

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""

import json
import sys
import time
import atexit

import logging

from griotte.scenario import _expect, _send, _unsubscribe_all

__WS__ = None

def play_video(media, sync=True):
    """ Plays video synchronously

    Plays video and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    global __WS__
    __WS__ = _send('video.command.start',
              '{ "media": "' + media + '" }',
              close=False)
    if sync:
        _expect(__WS__, 'video.event.stop')

def play_audio(media, sync=True):
    """ Plays sound synchronously

    Plays sound and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    global __WS__
    __WS__ = _send('video.command.start',
              '{ "media": "' + media + '" }',
              close=False,
              ws = __WS__)
    if sync:
        _expect(__WS__, 'video.event.stop')

def play_image(media, duration=0):
    """ Displays an image

    Displays an image for some time, or forever

    :param media: The media to play, relative to the media root folder
    :type media: str
    :param duration: The media to play, relative to the media root folder
    :type duration: int -- 0 for infinite
    """
    global __WS__
    __WS__ = _send('image.command.start',
                   '{ "media": "' + media + '" }',
                   ws = _WS__,
                   close=False)

def set_volume(level):
    """ Changes global volume

    Changes Griotte global volume

    :param level: The sound level, in percent (0 - 120)
    """
    global __WS__
    __WS__ = _send('meta.store.sound_level.set',
                   '{ "level":"%s" }' % int(level),
                   ws = __WS__,
                   close = False)

def stop_video():
    """ Stops currently playing video

    Sends a ws message asking for the video to stop
    """
    global __WS__
    __WS__ = _send('video.command.stop',
                   ws = __WS__,
                   close = False)

def stop_audio():
    """ Stops currently playing video

    Sends a ws message asking for the video to stop
    """
    global __WS__
    __WS__ = __send('audio.command.stop',
                    ws = __WS__,
                    close = False)

@atexit.register
def __goodbye__():
    global __WS__
    logging.debug("unloading")

    _unsubscribe_all(__WS__)
    __WS__.close()
