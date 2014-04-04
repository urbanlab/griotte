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

from griotte.ws import WebSocket
from setproctitle import setproctitle
from griotte.config import Config
import logging

class Handler:
    def __init__(self, name, watchdog_interval = 2):
        self._handler_name = name
        self._config = Config(name)
        setproctitle("griotte-%s" % name)

        self._ws = WebSocket(watchdog_interval = watchdog_interval)

        self._ws.add_listener("%s.command.ping" % self._handler_name,
                              self.ping)
        logging.debug("added ping listener for %s" % self._handler_name)

    def ping(self, channel, message):
        self._ws.send("%s.event.pong" % self._handler_name, { "handler": self._handler_name })
        logging.debug("%s sending pong" % self._handler_name)
