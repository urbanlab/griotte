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

"""

from griotte.scheduler import Scheduler
s = Scheduler()
s._start_subsystem("adc")


"""

import logging
from sys import exit
from griotte.ws import WebSocket
from subprocess import Popen, PIPE
from griotte.config import Config
from time import sleep

import signal

class Scheduler:
    """ Implements process scheduler that can start, stop, restart compoments

    Those components can be input, ouput handlers, but also scenarios.
    """

    def __init__(self):
        # Open websocket
        # Subcribe to proper channels (define them !)
        self._subsystems = dict()
        self._conf = Config('scheduler')
        self.ws = WebSocket(watchdog_interval=2)
        self.ws.add_listener('scheduler.command.start', self.start)
        self.ws.add_listener('scheduler.command.reload', self.reload)
        self.ws.add_listener('scheduler.command.restart', self.restart)
        self.ws.add_listener('scheduler.command.stop', self.stop)
        self.ws.add_listener('scheduler.command.shutdown', self.shutdown)
        self.ws.add_listener('scheduler.command.status', self.status)

        signal.signal(signal.SIGINT, self._signal)
        signal.signal(signal.SIGTERM, self._signal)
        signal.signal(signal.SIGUSR1, self._signal)
        signal.signal(signal.SIGHUP, self._signal)

        self._start()

    # ws handlers
    def start(self, channel, message):
        if 'daemons' in message and isinstance(message['daemons'], list):
            for d in message['daemons']:
                self._start_subsystem(d)

    def stop(self, channel, message):
        if 'daemons' in message and isinstance(message['daemons'], list):
            for d in message['daemons']:
                self._kill_subsystem(d)

    def reload(self, channel, message):
        if 'daemons' in message and isinstance(message['daemons'], list):
            self.start(channel, message)
            self.stop(channel, message)

    def restart(self, channel=None, message=None):
        logging.debug("restaring")
        self._restart()

    def shutdown(self, channel=None, message=None):
        logging.debug("shutting down")
        self._kill_server()
        self.ws.stop()
        exit(0)

    def status(self, channel, message):
        daemons = list()
        for subsys in self._conf:
            if subsys in ['DEFAULT']: continue
            daemons.push(subsys)

        self.ws.send('scheduler.event.status', { "alive": daemons })

    def _signal(self, sig, frame):
        logging.debug("received signal %s" % sig)
        if sig in [ signal.SIGUSR1, signal.SIGHUP ]:
            logging.debug("restarting")
            self._restart()
        elif sig in [ signal.SIGINT, signal.SIGTERM ]:
            self.shutdown()

    def _start(self):
        if 'server' not in self._subsystems:
            self._start_subsystem('server')
            self.ws.start()

        while not self.ws.is_ready():
            sleep(0.1)

        for subsys in self._conf:
            if subsys in ['DEFAULT', 'scheduler']: continue

            if self._conf[subsys]['start'] in ['true','yes'] and subsys not in self._subsystems:
                self._start_subsystem(subsys)

    def _restart(self):
        self._kill_subsystem()
        self._conf = Config('scheduler')
        self._start()

    def _kill_subsystem(self, name=None):
        if name is None:
            for subsys in list(self._subsystems):
                if subsys != 'server': self._kill_subsystem(subsys)
        else:
            logging.info("killing subsystem %s (pid %s)" % (name, self._subsystems[name].pid))
            self._subsystems[name].terminate()
            if self._subsystems[name].poll() is None:
                logging.info("hard killing subsystem %s (pid %s)" % (name, self._subsystems[name].pid))
                self._subsystems[name].kill()

            del self._subsystems[name]

    def _kill_server(self):
        # Killing the server is a one way trip since we have no way to restart it afterwards
        self._kill_subsystem()
        if self._subsystems['server'] is not None:
           self._subsystems['server'].kill()

    def _start_subsystem(self, name):
        full_path = "%s/%s" % (self._conf[name]['binaries_path'], name)
        self._subsystems[name] = Popen([full_path])
        logging.info("starting subsystem %s (pid %s)" % (name, self._subsystems[name].pid))


    def __del__(self):
        self._kill_server()


