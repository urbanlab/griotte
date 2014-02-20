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

import logging
import subprocess
import shlex

"""
Handles image display

Just a fbi spawner
"""
class Fbi(object):
    _LAUNCH_CMD = '/usr/bin/fbi -vt 1 -a -noverbose %s'

    def __init__(self):
        self._position_thread = None

        # Initialize status variables
        self.muted = False
        self.volume = self.amplitude = 0

    """
    Plays media by spawning fbi

    :param media: image to show
    """
    def play(self, mediafile):
        self.playing = False
        self.position = self.media_length = 0
        self.media = mediafile

        cmd = self._LAUNCH_CMD % mediafile
        args = shlex.split(cmd)

        pid = subprocess.Popen(args).pid
        logging.debug("launched cmd : %s in pid %s" % (cmd, pid))


