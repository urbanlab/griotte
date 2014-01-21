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

"""
..todo :: use static vars in functions
"""

_E = Expecter()

def get_analog(channel):
    """ Returns current analog value for channel

    This will block until an analog value is received on the requested channel

    :param channel: Channel to wait for
    """
    data = _E.send_expect("analog.command." + channel + ".periodic_sample",
                          "analog.event." + channel + ".sample",
                          data='{ "every": 0.5 }',
                          flush=True)

    # logging.debug("get_analog : expecting data")

    # data = _E.expect('analog.event.' + channel + '.sample', flush=True)

    logging.debug("get_analog : received sample %s" % data['raw_value'])

    return data['raw_value']

def set_profile(channel, profile):
    """ Sets the profile for channel
    """
    return

@atexit.register
def __goodbye__():
    _E.quit()

