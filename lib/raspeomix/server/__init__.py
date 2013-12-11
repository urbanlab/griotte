#
# (c) 2013 ERASME
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

import tornado.websocket
import logging
import json
from time import time
import fnmatch

"""
Messages:

/<topic>/<category>[/emitter]

topics : meta, command, message, event
 - meta : meta information (subscribing, connecting, storing values)
 - command : acting on something (video, actuator)
 - message : a regurlarly occuring message (sensor value, video playing progress, ...)
 - log : something logged that do not appear on the bus
categories for meta : subscribe, unsubscribe, join, ping, log, store
categories for command : sound, video, image, trigger, sensor (set profile, poll freq)
categories for message : value, video, sound
categories for event : io0-3/(raising|falling), an0-3(over_threshold|below_threshold), video (finish, pause), sound (finish, pause)

e.g. :

meta:subscribe { "channel" : ":event:io:1:rising" }
meta:store:sound_level { "value": 35 }
meta:store:some_complex { "value": { "complex": "data", "with": [ "array" ] } }
meta:store:date { "date" : 20140516, "time": "145232" }
meta:device:attach { "device" : "/dev/nfc1" }
meta:device:detach { "device" : "/dev/nfc1" }
request:an:2 { "profile???" }
command:video { "action" : "play", "media" : "wtf.mp4" }
message:video { "status" : "playing", "media" : "wtf.mp4", "progress" : "16", "length" : "49" }
message:an:0 { "value" : 146, "profile" : { "name" : "Maxborktik EZ-1", ... }}
message:nfc:1 { "value": "ab133df" }
event:io1:raising {}

All exchanged messages have a timestamp

"""
class Server(tornado.websocket.WebSocketHandler):
    """ Websocket Server """

    # Client hash
    clients          = {}
    # Channel hash, pointing to interested clients in sets
    channel_watchers = {}

    def open(self):
        Server._dispatch_all({  "channel":"meta:join",
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


        if decoded['channel'] == 'meta:subscribe':
            if Server.channel_watchers.get(decoded['data']['channel'], None) == None:
                Server.channel_watchers[decoded['data']['channel']] = set()
            # Handle subscribe
            logging.info("Got subscribe for channel %s" % decoded['data']['channel'])
            Server.channel_watchers[decoded['data']['channel']].add(self.key())
            Server._dump_channel_watchers()
        elif decoded['channel'] == 'meta:unsubscribe':
            # Handle unsusbscribe
            logging.info("Got unsubscribe for channel %s" % decoded['data']['channel'])
            Server.channel_watchers[decoded['data']['channel']].remove(self.key())
        else:
            Server._dispatch(decoded)

        #
    def on_close(self):
        logging.info("WebSocket closed for %s" % self.key())
        # remove client from list and from watchers
        Server._remove_channel_watcher(self.key())

        try:
            del(Server.clients[self.key()])
            Server._dispatch_all({  "channel":"meta:leave",
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
        if message['channel'] not in Server.channel_watchers:
            return
        for key in Server.channel_watchers[message['channel']]:
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

