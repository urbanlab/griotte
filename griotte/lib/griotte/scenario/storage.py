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

"""Server-side Storage groups blocks implementation

This module implements server-side code generated for storage blockly blocks.

.. module:: storage
   :platform: Unix

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""

from griotte.scenario import Expecter

def set_volume(level):
    """ Changes global volume

    Changes Griotte global volume

    :param level: The sound level, in percent (0 - 120)
    """
    Expecter().send('storage.set.sound_level', { "level": level })
