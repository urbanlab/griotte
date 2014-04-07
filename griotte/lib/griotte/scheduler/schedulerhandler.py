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
import json

from sys import exit
from griotte.config import Config
from time import sleep, time
from griotte.mediamanager import MediaManager
from griotte.handler import Handler
import tornado.ioloop

from griotte.subsystem import Subsystem
import signal

class Scheduler(Handler):
    """ Implements process scheduler that can start, stop, restart compoments

    Those components can be input, ouput handlers, but also scenarios.
    """

    def __init__(self):
        Handler.__init__(self)

        self._subsystems = dict()
        self._scenarios = dict()

        #self.ws = WebSocket(watchdog_interval=2)
        self._ws.add_listener('start')
        self._ws.add_listener('reload')
        self._ws.add_listener('restart')
        self._ws.add_listener('stop')
        self._ws.add_listener('shutdown')
        self._ws.add_listener('status')

        self._ws.add_listener('*.event.pong', full_path=True, callback=self._wscb_pong)

        signal.signal(signal.SIGINT, self._signal)
        signal.signal(signal.SIGTERM, self._signal)
        signal.signal(signal.SIGUSR1, self._signal)
        signal.signal(signal.SIGHUP, self._signal)

        self._start()

    # ws handlers
    def _wscb_start(self, channel, message):
        if 'daemons' in message and isinstance(message['daemons'], list):
            for d in message['daemons']:
                self._start_subsystem(d)

        if 'scenario' in message:
            self._start_scenario(message['scenario'])

    def _wscb_stop(self, channel, message):
        if 'daemons' in message and isinstance(message['daemons'], list):
            for d in message['daemons']:
                self._kill_subsystem(d)

        if 'scenario' in message:
            self._kill_scenario(s)

    def _wscb_reload(self, channel, message):
        if 'daemons' in message and isinstance(message['daemons'], list):
            self.start(channel, message)
            self.stop(channel, message)

    def _wscb_restart(self, channel=None, message=None):
        logging.debug("restaring")
        self._restart()

    def _wscb_shutdown(self, channel=None, message=None):
        logging.debug("shutting down")
        self._kill_server()
        self._subsystems = None
        self._ws.stop()
        exit(0)

    # TODO : send back something interesting...
    def _wscb_status(self, channel, message):
        daemons = list()
        for subsys in self._config:
            if subsys in ['DEFAULT']: continue
            daemons.push(subsys)

        self._ws.send('scheduler.event.status', { "alive": daemons })


    def _wscb_pong(self, channel, message):
        daemon = channel.split('.')[0]

        # We just don't care if it's us
        # Using self._handler_name just in case someone changes it's mind
        # on the name
        if daemon == self._handler_name:
            return

        logging.debug("just had pong from subsystem %s" % daemon)
        self._subsystems[daemon].latency   = time() - message['timestamp']
        self._subsystems[daemon].last_seen = message['timestamp']

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
            self._ws.start()

        while not self._ws.is_ready():
            sleep(0.1)

        for subsys in self._config:
            if subsys in ['DEFAULT', 'scheduler']: continue

            if self._config[subsys]['start'] in ['true','yes'] and subsys not in self._subsystems:
                self._start_subsystem(subsys)


        pinger = tornado.ioloop.PeriodicCallback(self._ping_subsystems,
                                                5000,
                                                io_loop = tornado.ioloop.IOLoop.instance())
        pinger.start()
        self._autostart_scenarios()

    def _ping_subsystems(self):
        if not self._ws.is_ready():
            logging.warning("ws is not ready to send")
            return

        for subsys in list(self._subsystems):
            self._ws.send("%s.command.ping" % name, {})

            if self._subsystems[name].last_seen is None:
                logging.warning("%s was never seen" % name)
            else:
                logging.debug("%s was last seen %s seconds ago" % (name, time() - self._subsystems[name].last_seen))

        logging.debug("sent ping to all known subsystems")

    def _autostart_scenarios(self):
        """ Advertises scenarios that have to run at start
        """
        for sc in json.loads(MediaManager.get('scenario')):
            if 'autostart' in sc and sc['autostart'] == True:
                self._start_scenario(sc)

    def _restart(self):
        self._kill_subsystem()
        self._config = Config('scheduler')
        self._start()

    def _kill_subsystem(self, name=None):
        if 'skip_daemons' in self._config['scheduler'] and self._config['scheduler']['skip_daemons'] not in ['no', 'false']:
            return

        if name is None:
            for subsys in list(self._subsystems):
                if subsys != 'server': self._kill_subsystem(subsys)
        else:
            logging.info("killing subsystem %s (pid %s)" % (name, self._subsystems[name].pid))
            del self._subsystems[name]

    def _kill_scenario(self, name=None):
        if name is None:
            for scen in list(self._scenarios):
                self._kill_scenario(subsys)
        else:
            logging.info("killing scenario %s (pid %s)" % (name, self._scenario[name].pid))
            del self._scenario[name]

    def _kill_server(self):
        # Killing the server is a one way trip since we have no way to restart it afterwards
        self._kill_subsystem()
        if self._subsystems['server'] is not None:
           del self._subsystems['server']

    def _start_subsystem(self, name):
        if 'skip_daemons' in self._config['scheduler'] and self._config['scheduler']['skip_daemons'] not in ['no', 'false']:
            return

        full_path = "%s/%s" % (self._config[name]['binaries_path'], name)
        self._subsystems[name] = Subsystem(name, full_path)

    def _start_scenario(self, scenario):
        name = scenario['name']
        self._scenarios[name] = Subsystem(name, scenario['path'], scenario = True)
        logging.info("starting scenario %s (pid %s)" % (name, self._scenarios[name].pid))

    def __del__(self):
        self._kill_server()


