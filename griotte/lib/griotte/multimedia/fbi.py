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
import atexit

"""
Handles image display

Just a fbi spawner
"""
class Fbi(object):
    _LAUNCH_CMD = ['/usr/bin/fbi', '-vt', '1', '-a', '-noverbose', '-1' ]

    def __init__(self):
        self._popen = None

        # Clean up framebuffer
        logging.info("Clearing framebuffer")
        subprocess.Popen(['setterm', '-cursor', 'off'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.Popen("echo 0 > /sys/class/graphics/fbcon/cursor_blink",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.Popen(['dd', 'if=/dev/zero', 'of=/dev/fb0'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    """
    Plays media by spawning fbi

    :param mediafile: image to show
    """
    def play(self, mediafile):
        self.media = mediafile
        cmd = self._LAUNCH_CMD + [ mediafile ]

        if self._popen:
            logging.debug("terminating existing instance %s" % self._popen.pid)
            # Sorry, I have nothing better
            # fni forks/detach itself and gets out of control
            self._popen = subprocess.Popen(['/usr/bin/killall','fbi'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            self._popen.communicate()[0]
            self._popen.wait()
            logging.debug("instance terminated with code %s" % self._popen.returncode)

        self._popen = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.debug("launched cmd : %s in pid %s" % (" ".join(cmd), self._popen.pid))

@atexit.register
def __goodbye__():
    logging.info("Killing leftover fbi instances")
    subprocess.Popen(['/usr/bin/killall','fbi']).wait()
    logging.info("Restoring fb cursor")
    subprocess.Popen("echo 1 > /sys/class/graphics/fbcon/cursor_blink",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
