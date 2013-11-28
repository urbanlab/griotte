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
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import tornado.websocket
import json

class Server(tornado.websocket.WebSocketHandler):
    """ Websocket Server """

    clients=set()

    def open(self):
        print("WebSocket opened")
        for con in Server.clients:
            con.write_message(json.dumps({"type":"presence"}))

        Server.clients.add(self)
        print("Handling %s clients" % len(Server.clients))


    def on_message(self, message):
        print("Received : %s" % message)
        #self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
        try:
            Server.clients.remove(self)
        except Exception:
            print("error closing connection for client")
