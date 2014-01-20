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


import tornado.websocket
import logging
import json
from time import time
import fnmatch

"""
Server class

Handles channel subscription and message dispathing to clients.

See :doc:`messages` for more info on messages.

"""
class Server(tornado.websocket.WebSocketHandler):
    """ Websocket Server """

    # Client hash
    clients          = {}
    # Channel hash, pointing to interested clients in sets
    channel_watchers = {}

    def open(self):
        Server._dispatch_all({  "channel":"meta.join",
                                "timestamp": time(),
                                "data": { "client": self.key() }
                            })

        key = self.key()
        Server.clients[key] = self

        logging.info("WebSocket opened for %s" % key)
        logging.info("Currently handling %s clients" % len(Server.clients))

    def on_message(self, message):
        logging.debug("Received : %s" % message)

        decoded = None

        try:
            decoded = json.loads(message)
        except ValueError:
            logging.error("Unable to decode crappy JSON: %s" % message)

        if decoded is None:
            return

        # Check server-related messages
        if decoded['channel'] == 'meta.subscribe':
            if Server.channel_watchers.get(decoded['data']['channel'], None) == None:
                Server.channel_watchers[decoded['data']['channel']] = set()
            # Handle subscribe
            logging.info("Got subscribe for channel %s" % decoded['data']['channel'])
            Server.channel_watchers[decoded['data']['channel']].add(self.key())
            Server._dump_channel_watchers()
        elif decoded['channel'] == 'meta.unsubscribe':
            # Handle unsusbscribe
            logging.info("Got unsubscribe for channel %s" % decoded['data']['channel'])
            Server.channel_watchers[decoded['data']['channel']].remove(self.key())
        else:
            Server._dispatch(decoded)

    def on_close(self):
        logging.info("WebSocket closed for %s" % self.key())
        # remove client from list and from watchers
        Server._remove_channel_watcher(self.key())

        try:
            del(Server.clients[self.key()])
            Server._dispatch_all({  "channel":"meta.leave",
                                    "timestamp": time(),
                                    "data": { "client": self.key() }
                                })
        except Exception as ex:
            logging.error("Error closing connection for client : %s" % ex)

        logging.info("Currently handling %s clients" % len(Server.clients))

    def key(self):
        return ("%s#%s" % (str(self.request.remote_ip),
                         str(self.request.connection.address[1])))

    @staticmethod
    def _dispatch_all(message):
        for con in Server.clients:
            Server.clients[con].write_message(message)

    @staticmethod
    def _dispatch(message):
        # We have to check the wildcards
        message_channel = message['channel']

        # Clients can watch wildcard channels
        for watched_channel in Server.channel_watchers:
            if fnmatch.fnmatch(message_channel, watched_channel):
                # We had a match for watched_channel key
                # We have to iterate over client list for this channel
                for key in Server.channel_watchers[watched_channel]:
                    logging.debug("Dispatching message to %s" % key)
                    Server.clients[key].write_message(json.dumps(message))

    @staticmethod
    def _remove_channel_watcher(key):
        # Remove watcher from channel
        for channel, clientset in Server.channel_watchers.items():
            clientset.discard(key)
        # Remove unused channels
        Server.channel_watchers = dict((k, v) for k, v in Server.channel_watchers.items() if v)

    @staticmethod
    def _dump_channel_watchers():
        for channel, clientset in Server.channel_watchers.items():
            clients = ""
            for key in clientset:
                clients += "," + key
            logging.debug("%s : {%s}" % (channel, clients[1:]))

