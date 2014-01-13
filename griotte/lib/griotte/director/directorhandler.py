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

"""Scenario spawner module

This module spawns required scenarios.
It can be invoked at boot or at runtime.

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

.. note:: Use http://docs.python.org/3.3/library/multiprocessing.html ?
"""

import threading
import logging

class DirectorHandler:
    """ Scenario handling class

    Spawns and kills scenario on demand
    """

    def __init__(self):
        logging.error("To Be Written")
