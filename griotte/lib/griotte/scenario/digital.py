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

"""Server-side Analog groups blocks implementation

This module implements server-side code generated for analog sensors blockly blocks.

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""

import sys
import time

import logging
import atexit

from griotte.scenario import Expecter

def get_digital(port):
    """ Returns current digital value for port

    This will block until a digital value is received on the requested port

    :param port: port to wait for
    """
    data = Expecter().send_expect("digital.command." + port + ".sample",
                                  "digital.event." + port + ".sample",
                                  data  = { "every": 0.5 },
                                  flush = True)

    logging.debug("get_digital : received sample %s" % data['value'])

    return data['value']

def wait_edge(port, style="any"):
    """ Waits for an edge (rising, falling, any) on a port

    This will block until an edge of the requested style is sensed on the requested port

    :param port: port to wait for
    :type port: str
    :param style: type of edge to wait for ('rising', 'falling' of 'any')
    :type style: str
    """
    if style not in ('rising', 'falling','any'):
        raise ValueError("edge argument can only be 'rising', 'falling' of 'any'")

    if style == 'any':
        data = Expecter().expect("digital.event." + port + ".edge.*",
                                 flush = True)
    else:
        data = Expecter().expect("digital.event." + port + ".edge." + style,
                                 flush = True)

    logging.debug("get_digital : received edge %s for port %s" % (data['value'], port))

    return data['value']

def set_profile(port, profile):
    """ Sets the profile for port
    """
    return

@atexit.register
def __goodbye__():
    Expecter().quit()

