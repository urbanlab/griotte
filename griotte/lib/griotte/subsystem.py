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

from subprocess import Popen, PIPE
import logging

class Subsystem:
    def __init__(self, name, path, handler = True, scenario = False):
        self.name = name
        self.path = path
        self.last_seen = None
        self.latency = float("inf")
        self.popen = None

        if scenario:
            command = ['python3', self.path]
        elif handler:
            command = ["%s/griotte" % self.path, self.name]
        else:
            command = ["%s/%s" % (self.path, self.name)]

        logging.info("executing '%s' for %s" % (' '.join(command), self.name))
        try:
            self.popen = Popen(command)
        except OSError as e:
            logging.error("Error %s executing '%s' : %s" % (e.errno, ' '.join(command), e.strerror))

        self.pid = self.popen.pid
        logging.info("subsystem %s (pid %s) started" % (self.name, self.pid))

    def __del__(self):
        self.popen.terminate()
        if self.popen.poll() is None:
            logging.info("subsystem %s (pid %s) suiciding" % (self.name, self.pid))
            self.popen.kill()
