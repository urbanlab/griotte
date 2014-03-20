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
import fnmatch
import os
import re

from subprocess import Popen, PIPE
from shutil import copyfile

import griotte.graceful
from griotte.multimedia.mediamanager import MediaManager
from tornado.options import options
from time import time

class Api(tornado.web.RequestHandler):
    def get(self, target):
        self.write(MediaManager.get(target))


#### TODO: This should definitively get out of here and go into mediamanager.py
class MediaProcessor:
    _VIDEO_CMD = "/usr/bin/avconv -i %s -vf scale='min(300\,iw):-1' -ss 00:00:05 -f image2 -vframes 1 %s_thumbnail.jpg"
    _IMAGE_CMD = "/usr/bin/avconv -i %s -vf scale='min(300\,iw):-1' -f image2 -vframes 1 %s_thumbnail.jpg"
    _THUMBNAILER_SQUARE_CMD = "/usr/bin/avconv -i %s -vf crop='min(iw\,ih):min(iw\,ih)' -f image2 -vframes 1 %s_square_thumbnail.jpg"
    _AUDIO_CMD = "/usr/bin/avprobe %s"

    _VIDEOPROP_REXP       = re.compile(b"\s*([\w]+)\s*:\s*(.*)")
    _VIDEOPROP_REXP_START = re.compile(b"Input #0.*")
    _VIDEOPROP_REXP_STOP  = re.compile(b"Output #0.*")

    def __init__(self, path, mime):
        self._family, self._type = mime.split('/')
        self._media = path
        if (self._family == "video"):
            self._process_media(self._VIDEO_CMD % (self._media, self._media))
            Popen(self._THUMBNAILER_SQUARE_CMD % (self._media, self._media), shell=True)
        elif (self._family == "image"):
            self._process_media(self._IMAGE_CMD % (self._media, self._media))
            Popen(self._THUMBNAILER_SQUARE_CMD % (self._media, self._media), shell=True)
        else:
            self._process_media(self._AUDIO_CMD % self._media)

    def _process_media(self, cmd, thumbnail=None):
        started_at = time()
        pipe = Popen(cmd, shell=True, stderr=PIPE)
        metadata = {}
        in_input = False
        for line in pipe.stderr:
            if in_input:
                m = self._VIDEOPROP_REXP.match(line)
                if m:
                    key, value = m.groups()
                    metadata[key.decode('ascii')] = value.decode('ascii')
            if self._VIDEOPROP_REXP_START.match(line):
                in_input = True
            elif self._VIDEOPROP_REXP_STOP.match(line):
                in_input = False

        # Duration needs special processing
        if 'Duration' in metadata:
          info = metadata['Duration'].split(', ')
          # Re-add duration as key
          info[0] = "duration: %s" % info[0]
          for i in info:
            k,v = i.split(': ')
            metadata[k] = v
        metadata.pop("Duration", None)
        metadata.pop("Metadata", None)

        f = open("%s_meta.json" % self._media, 'w')
        json.dump(metadata, f)
        f.close()
        logging.info("thumbnail and metadata processed for file %s in %s seconds" %
                     (self._media, time() - started_at))

class Uploader(tornado.web.RequestHandler):

    def _process_media(self, path, mime):
        MediaProcessor(path, mime)

    def post(self):
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        mime = fileinfo['content_type']
        #extn = os.path.splitext(fname)[1]

        logging.debug("got upload request with file %s" % fname)

        subpath = mime.split('/')[0]

        if not subpath in ['video','image','audio']:
            logging.warning("unsupported content-type %s for file %s" % (mime, fname))
            self.send_error(415)
            return

        path = "%s/%s/" % (options.store, subpath)

        if not os.path.isdir(path):
            os.mkdir(path)

        fname = re.sub('[ /,;]', '_', fname)
        path = "%s/%s" % (path, fname)

        fh = open(path, 'wb')
        fh.write(fileinfo['body'])
        fh.close()

        logging.debug("%s uploaded to %s" % (fname, options.store))
        #self.redirect("%s#page-medias" % self.request.headers.get('Referer'))

        # start & detach a process :
        # avconv -i ~/video.m4v -vf scale='min(180\,iw):-1' -ss 00:00:05 -f image2 -vframes 1 thumbnail.jpg
        with tornado.stack_context.NullContext():
            tornado.ioloop.IOLoop.instance().add_callback(self._process_media, path, mime)

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

        logging.debug("WebSocket opened for %s" % key)
        logging.debug("Currently handling %s clients" % len(Server.clients))

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
            #Server._dump_channel_watchers()
        elif decoded['channel'] == 'meta.unsubscribe':
            # Handle unsusbscribe
            logging.info("Got unsubscribe for channel %s" % decoded['data']['channel'])
            Server.channel_watchers[decoded['data']['channel']].remove(self.key())
        else:
            Server._dispatch(decoded)

    def on_close(self):
        logging.debug("WebSocket closed for %s" % self.key())
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

        logging.debug("Currently handling %s clients" % len(Server.clients))

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

