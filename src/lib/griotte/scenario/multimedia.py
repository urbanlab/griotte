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

import logging

from websocket import create_connection

def play_video(media, sync=True):
    """ Plays video synchronously

    Plays video and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    ws = _send('video.command.start',
              '{ "media": "' + media + '" }',
              close=False)
    if sync:
        _expect(ws, 'video.event.stop')

def play_audio(media, sync=True):
    """ Plays sound synchronously

    Plays sound and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    ws = _send('video.command.start',
              '{ "media": "' + media + '" }',
              close=False)
    if sync:
        _expect(ws, 'video.event.stop')

def play_image(media, duration=0):
    """ Displays an image

    Displays an image for some time, or forever

    :param media: The media to play, relative to the media root folder
    :type media: str
    :param duration: The media to play, relative to the media root folder
    :type duration: int -- 0 for infinite
    """
    ws = _send('image.command.start',
              '{ "media": "' + media + '" }',
              close=False)

def set_volume(level):
    """ Changes global volume

    Changes Griotte global volume

    :param level: The sound level, in percent (0 - 120)
    """
    _send('meta.store.sound_level.set',
         '{ "level":"%s" }' % int(level))

def stop_video():
    """ Stops currently playing video

    Sends a ws message asking for the video to stop
    """
    _send('video.command.stop')

def stop_audio():
    """ Stops currently playing video

    Sends a ws message asking for the video to stop
    """
    _send('audio.command.stop')

def _send(channel, data = '{}', close=True, ws=None):
    """ Sends a message over websocket

    Utility function that wraps websocket message sending and takes care of
    opening a websocket if needed

    :param channel: The channel to write to
    :type channel: str.

    :param data: The data to send
    :type data: str -- json encoded

    :param close: Whether the socket must be closed after sending the message
    :type close: bool

    :param ws: A websocket to use. If `None`, a websocket will be created.
    :type ws: WebSocket

    :returns: WebSocket object, or None if close was True.
    """
    # Open websocket if we're not given one
    if ws == None:
        ws = create_connection("ws://localhost:8888/ws")

    print(data)
    decoded = json.loads(data)

    data = json.dumps( { 'channel': channel, 'data': decoded } )
    logging.debug("in channel %s sending %s" % (channel, data))
    ws.send(data)

    if close:
        ws.close()
        return None

    return ws

def _expect(ws, channel, type=None):
    data = json.dumps( { 'channel': 'meta.subscribe',
                         'timestamp': time.time(),
                         'data': { 'channel': channel } } )
    ws.send(data)

    found = False
    while not found:
        message = ws.recv()
        decoded = json.loads(message)
        if decoded['channel'] == channel and decoded['data']['type'] == type:
            found = True;
