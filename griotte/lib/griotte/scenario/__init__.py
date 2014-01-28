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

This module implements socket communications for scenarios.

**A word on this implementation**

At first sight, it could seem quite trivial. Just use the ws.recv() blocking
call and wait for data to arrive before returning back to the caller function in
the scenario (e.g. `griotte.scenario.digital.get_digital`).

However, consider the following scenario :

.. code-block:: python

  while True:
    if get_digital('io0'):
      play_video('kitten.mp4', sync=True)

`get_digital` waits (calling `expect` here) for some value, and then
`play_video` is called. Since the call is `sync=True`, the scenario will block
until video finishes.

When the video finishes, `get_digital` is called again; it will call ws.recv()
which will return immediately since there would be a pile of data waiting in the
websocket buffer. But the first data that will be used will be the data sent by
the digital backend just after the one that passed the test, and it will
probably be the same value and the video will plya again. We've just recreated a
software equivalent of hardware bouncing.

Since there is no non-blocking recv call in websocket client (which would let us
empty the websocket bufffer before waiting for new values), we have to find
annother way.

The approach used here is the following :

- start a threaded websocket client
- when a message arrives, add it in a dedicated Queue object for that channel
- when a `expect` is called with `flush=True`, the Queue for the considered
  channel is flushed and `expect` will wait until a new value arrives.

This is much more complex, but until a non-blocking recv call is implemented in
websocket client (which would let us empty the websocket bufffer before waiting
for new values), we have to find annother way.

"""

import json
import logging
import time

from queue import Queue
from griotte.ws import WebSocket

import griotte.graceful

class Expecter:
    class __Expecter:
        """ Utility class that sends and receives data over websocket for server-side blocks

        """
        def __init__(self, uri=None):
            self._ws = WebSocket(watchdog_interval=2, uri=uri)
            self._ws.start()
            self._subscriptions = {}

        def send_expect(self, channel_out, channel_in, data='{}', flush=False):
            """ Sends a message over websocket and waits for a reply

            A combination of :py:func:`send` and :py:func:`expect`

            :param channel_out: The channel to write to
            :type channel: str

            :param channel_in: The channel to listen to
            :type channel: str

            :param data: The data to send
            :type data: str -- json encoded

            :param flush: Whether the incoming queue must be flushed before handling message (set to True to prevent receiving past messages )
            :type flush: bool
            """

            self._subscribe(channel_in)

            if flush:
                self._flush_queue(channel_in)

            self._ws.send(channel_out, data)
            return self._subscriptions[channel_in].get()

        def send(self, channel, data = '{}'):
            """ Sends a message over websocket

            Utility function that wraps websocket message sending and takes care of
            opening a websocket if needed

            :param channel: The channel to write to
            :type channel: str.

            :param data: The data to send
            :type data: str -- json encoded

            :param flush: Whether the incoming queue must be flushed before handling message (set to True to prevent receiving past messages )
            :type flush: bool
            """

            logging.debug("sending message on %s" % channel)
            self._ws.send(channel, data)

        def expect(self, channel, flush=False):
            """ Expects a message on a channel

            Blocks until the message arrives and returns the 'data' part of the message

            :param channel: Channel to listen to
            :type channel: str

            :param flush: Whether the incoming queue must be flushed before handling message (set to True to prevent receiving past messages )
            :type flush: bool

            :rtype: dict -- the message we got on the wire
            """

            self._subscribe(channel)

            if flush:
                self._flush_queue(channel)

            data = self._subscriptions[channel].get()
            logging.debug("got message on %s" % channel)

            #self._unsubscribe(channel)

            return data

        def quit(self):
            self._unsubscribe_all()
            self._ws.stop()

        def on_message(self, channel, data):
            print("message on channel %s" % channel)

            try:
                self._subscriptions[channel].put(data)
            except KeyError:
                logging.error("Received a message for a channel we didn't subsribe to (%s)" % channel)

        def _flush_queue(self, channel):
            logging.debug("Flushing queue for channel %s" % channel)

            try:
                while not self._subscriptions[channel].empty():
                    self._subscriptions[channel].get()
                    logging.debug("flushed one message")
            except Empty:
                return

        def _subscribe(self, channel):
            if channel in self._subscriptions:
                return False

            self._subscriptions[channel] = Queue()

            logging.debug("subscribing to channel %s" % channel)
            self._ws.add_listener(channel, self.on_message)

            return True

        def _unsubscribe(self, channel):
            if channel not in self._subscriptions:
                return

            logging.debug("unsubscribing from channel %s" % channel)

            self._ws.remove_listener(channel)

            logging.debug("removing channel %s" % channel)
            self._subscriptions.pop(channel)

        def _unsubscribe_all(self):
            for channel in self._subscriptions.copy().keys():
                self._unsubscribe(channel)

    instance = None
    def __new__(cls):
        if not Expecter.instance:
            Expecter.instance = Expecter.__Expecter()
        return Expecter.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)
