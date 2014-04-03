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

"""Server-side RFID group blocks implementation

This module implements server-side code generated for RFID reader
 blockly blocks.

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""

import sys
import time

import logging
import atexit

from griotte.scenario import Expecter

def rfid_read(tag):
    """ Returns when tag is read

    This will block until a tag is read on the RFID reader

    :param tag: tag to wait for. If None, will return first tag seen
    :rtype: string -- tag read on reader
    """

    while True:
        data = Expecter().expect("rfid.event.tag",
                                 flush = True)

        logging.debug("rfid_read : received tag %s" % data['tag'])

        if tag == None or tag == data['tag']:
            return data['tag']

@atexit.register
def __goodbye__():
    Expecter().quit()

