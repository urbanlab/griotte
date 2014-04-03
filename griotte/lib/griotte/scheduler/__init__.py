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
import os
import pygame
from time import sleep


from subprocess import Popen, PIPE
from griotte.multimedia.pgimage import PgImage

class Scheduler:
    """ Implements process scheduler that can start, stop, restart compoments

    Those components can be input, ouput handlers, but also scenarios.
    """

    def __init__(self):
        # Open websocket
        # Subcribe to proper channels (define them !)
        self._pg = PgImage()
        self._pg.play('/home/pi/keep-calm.png')
        sleep(20)


