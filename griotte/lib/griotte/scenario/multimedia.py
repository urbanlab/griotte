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

from griotte.scenario import Expecter

def set_background(strhex):
    """ Displays image

    Plays displays image returns

    :param media: The image to show, relative to the media root folder
    """
    logging.info("Setting background to %s" % strhex)
    Expecter().send('image.command.background', { "color": strhex })

def play_image(media, duration=0):
    """ Displays image

    Plays displays image returns

    :param media: The image to show, relative to the media root folder
    """
    logging.info("Playing image %s" % media)
    Expecter().send('image.command.start', { "media": media })

def play_video(media, sync=True):
    """ Plays video synchronously

    Plays video and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    Expecter().send('video.command.start', { "media": media })

    if sync:
        print("sync mode, expecting stop")
        Expecter().expect('video.event.stop')

def play_audio(media, sync=True):
    """ Plays sound synchronously

    Plays sound and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    Expecter().send('video.command.start', { "media": media })
    if sync:
        Expecter().expect('video.event.stop')

def set_volume(level):
    """ Changes global volume

    Changes Griotte global volume

    :param level: The sound level, in percent (0 - 120)
    """
    Expecter().send('storage.set.sound_level', { "level": level })

def stop_video():
    """ Stops currently playing video

    Sends a ws message asking for the video to stop
    """
    Expecter().send('video.command.stop')

def stop_audio():
    """ Stops currently playing video

    Sends a ws message asking for the video to stop
    """
    Expecter().send('audio.command.stop')

@atexit.register
def __goodbye__():
    Expecter().quit()
