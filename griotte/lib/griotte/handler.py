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

class Handler:
    def __init__(self, name):
        self._handler_name = name
        self._ws = WebSocket(watchdog_interval=2)

        self._ws.add_listener("%s.command.ping" % self._handler_name,
                              self.ping)

    def ping(self):
        self._ws.send("%s.event.pong", '{}')
