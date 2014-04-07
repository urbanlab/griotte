#
# (c) 2013-2014 ERASME
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
# along with Raspeomix.  If not, see <http://www.gnu.org/licenses/>.

from griotte.config import Config
from griotte.websocket import WebSocket

from setproctitle import setproctitle

import logging

class Handler:
    def __init__(self):

        # Check is class name is properly constructed
        # like SomethingHandler
        if (self.__class__.__name__[-7:] != 'Handler'):
            raise ValueError("Wrong handler class name : must be [something]Handler")

        self._handler_name = (self.__class__.__name__)[0:-7].lower()
        self._config = Config(self._handler_name)

        logging.debug("Initializing Handler's base for %s" % self._handler_name)
        setproctitle("griotte-%s" % self._handler_name)

        self._ws = WebSocket()
        self._ws.add_listener("%s.command.ping" % self._handler_name, self.ping)
        logging.debug("Added ping listener for %s" % self._handler_name)

    def ping(self, channel, message):
        self._ws.send("%s.event.pong" % self._handler_name, { "handler": self._handler_name })
        logging.debug("%s sending pong" % self._handler_name)

    def send_event(self, event, data):
        self._ws.send("%s.event.%s" % (self._handler_name, event), data)

    def add_listener(self, command, full_path=False, callback=None):
        if callback is None:
            callback = getattr(self, "_wscb_%s" % command.split(".")[-1])

        if full_path:
            path = full_path
        else:
            path = "%s.command.%s" % (self._handler_name, command)

        self._ws.add_listener(path, callback)
