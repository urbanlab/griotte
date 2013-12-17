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
# along with Raspeomix. If not, see <http://www.gnu.org/licenses/>.

import json

from websocket import create_connection
try:
    import RPIO
except SystemError:
    print("Mocking RPIO")

class GPIO:
    """ GPIO handler """

    # Pin to board
    IO = [ 12, 11, 13, 15 ]
    DIP = [ 7, 16 ]

    def __init__(self, wsclient):
        self.ws = wsclient

