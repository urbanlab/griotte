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

"""Server-side blocks implementation

This module implements server-side code generated for blockly blocks.

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""

# Why ?? Let the generator do the stuff
# import griotte.scenario.analog
# import griotte.scenario.digital
# import griotte.scenario.multimedia

import json
import logging
import time

from websocket import create_connection

__SUBSCRIPTIONS__ = []

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

    decoded = json.loads(data)

    data = json.dumps( { 'channel': channel, 'data': decoded } )
    logging.debug("in channel %s sending %s" % (channel, data))

    ws.send(data)

    if close:
        ws.close()
        return None

    return ws

def _expect(ws, channel):
    """ Expects a message on a channel

    Blocks until the message arrives and returns the 'data' part of the message

    :param ws: websocket to use
    :type ws: Websocket object
    :param channel: Channel to listen to
    :type channel: str
    :rtype: dict
    """
    global __SUBSCRIPTIONS__

    __subscribe(ws,channel)

    # Open websocket if we're not given one
    if ws == None:
        ws = create_connection("ws://localhost:8888/ws")

    if channel not in __SUBSCRIPTIONS__:
        __SUBSCRIPTIONS__.append(channel)

    found = False
    while not found:
        message = ws.recv()
        decoded = json.loads(message)
        if decoded['channel'] == channel:
            found = True;

    __unsubscribe(ws,channel)

    return decoded['data']

def __subscribe(ws, channel):
    data = json.dumps( { 'channel': 'meta.subscribe',
                         'timestamp': time.time(),
                         'data': { 'channel': channel } } )
    ws.send(data)

def __unsubscribe(ws, channel):
    data = json.dumps( { 'channel': 'meta.unsubscribe',
                         'timestamp': time.time(),
                         'data': { 'channel': channel } } )
    ws.send(data)

def _unsubscribe_all(ws):
    global __SUBSCRIPTIONS__

    for channel in __SUBSCRIPTIONS__:
        __unsubscribe(ws, channel)
        time.sleep(1)


