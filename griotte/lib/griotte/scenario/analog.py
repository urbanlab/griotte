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

import json
import sys
import time

import logging
import atexit

from griotte.scenario import _expect, _send, _unsubscribe_all

__WS__ = None

def get_analog(channel):
    """ Returns current analog value for chanel

    This will block until an analog value is received on the requested channel

    :param channel: Channel to wait for
    """
    global __WS__

    __WS__ = _send("analog.command." + channel + ".periodic_sample",
          data = '{ "every": 0.1 }', close=False, ws=__WS__)

    logging.debug("expecting data...")
    data = _expect(__WS__, 'analog.event.' + channel + '.sample')
    logging.debug("received sample %s" % data['raw_value'])

    return data['raw_value']

def set_profile(channel, profile):
    """ Sets the profile for channel
    """
    return

@atexit.register
def __goodbye__():
    global __WS__

    if not __WS__:
        return

    logging.debug("unloading")

    _unsubscribe_all(__WS__)
    __WS__.close()

