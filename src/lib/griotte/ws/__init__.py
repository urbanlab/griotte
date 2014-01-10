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

import json
import socket
import time
import griotte.constants as C
import logging

import fnmatch

import threading
import websocket

class WebSocket:
    """ WebSocket client """


    def __init__(self, watchdog_interval=0):
        self.callbacks = dict()
        #websocket.enableTrace(True)
        url = "ws://" + C.DEFAULT_SERVER + ":" + C.DEFAULT_PORT + "/ws"
        logging.info("Using server at %s" % url)
        self.ws = websocket.WebSocketApp(url,
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close)

        self.ws.on_open = self.on_open
        self.watchdog_interval = watchdog_interval
        if self.watchdog_interval > 0:
            logging.info("Watchdog interval set to %ss" % self.watchdog_interval)

    def start(self):
        logging.info("Starting websocket client thread")
        self.websocket_thread = threading.Thread(target=self.ws.run_forever, args=())
        #self.websocket_thread.daemon = True
        self.websocket_thread.start()

    def stop(self):
        self.watchdog_interval=0
        self.ws.close()

    def add_listener(self, channel, callback, *args):
        """ Adds a listener to a specific or wildcar channel

        :param channel: Channel to watch
        :param callback: Callback method
        :param args: Callback additionnal arguments
        :type args: array

        .. note:: There can be only one listener on a specific channel
        """

        logging.debug("Adding callback for channel %s", channel)
        self.callbacks[channel] = callback

    def send(self, channel, message):
        data = json.dumps( { 'channel': channel,
                             'timestamp': time.time(),
                             'data': message } )
        self.ws.send(data)

    # def on_message(self, ws, message):
    #     """ Decodes incoming message and dispatches to local callback """
    #     logging.debug("Received : %s" % message)
    #     decoded = json.loads(message)
    #     if (decoded['channel'] in self.callbacks.keys()):
    #         logging.debug("Callback found for channel %s, dispatching" % decoded['channel'])
    #         self.callbacks[decoded['channel']](decoded['channel'], decoded['data'])

    def on_message(self, ws, message):
        """ Decodes incoming message and dispatches to local callback """
        logging.debug("Received : %s" % message)
        decoded = json.loads(message)

        # We have to check the wildcards
        message_channel = decoded['channel']

        # Clients can watch wildcard channels
        for watched_channel in self.callbacks.keys():
            if fnmatch.fnmatch(message_channel, watched_channel):
                # We had a match for watched_channel key
                logging.debug("Dispatching message for channel %s" % message_channel)
                self.callbacks[watched_channel](decoded['channel'], decoded['data'])

    def on_error(self, ws, error):
        logging.error("Websocket error : %s" % error)

    def on_close(self, ws):
        logging.warning("Websocket closed")

        if self.watchdog_interval > 0 :
            logging.info("Starting websocket watchdog thread")
            self.watchdog_thread = threading.Thread(target=self._watchdog, args=())
            #self.watchdog_thread.daemon = True
            self.watchdog_thread.start()
        else:
            message = "Watchdog is off"

    def on_open(self, ws):
        logging.info("Websocket opened")
        # Subscribe to requested channels
        for channel in self.callbacks.keys():
            self._subscribe(channel)

    def _watchdog(self):
        logging.warning("Watchdog will try reconnecting in %s seconds" %self.watchdog_interval)

        time.sleep(self.watchdog_interval)

        if not self.websocket_thread.is_alive():
            logging.warning("Websocket thread is dead, restarting")
            self.start()

    def _subscribe(self, channel):
        self.send('meta.subscribe', { 'channel': channel })

    def debug(self):
        print ("hello %s",__main__)

if __name__ == "__main__":
    # test code
    import tornado.options
    def func(message):
        print("in callback with %s" % message)

    tornado.options.parse_command_line()
    ws = WebSocket(watchdog_interval=2)
    ws.add_listener('an', func)
    ws.start()
