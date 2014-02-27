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

"""Server-side Image groups blocks implementation

This module implements server-side code generated for image blockly blocks.

.. module:: multimedia
   :platform: Unix

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""

import atexit

from griotte.scenario import Expecter

def play_image(media):
    """ Displays image

    Plays displays image returns

    :param media: The image to show, relative to the media root folder
    """
    logging.info("Playing image %s" % media)
    Expecter().send('image.command.start', { "media": media })

def blank_screen():
    """ Displays image

    Plays displays image returns

    :param media: The image to show, relative to the media root folder
    """
    logging.info("Blanking screen")
    Expecter().send('image.command.start', { "media": "blank.png" })

@atexit.register
def __goodbye__():
    Expecter().quit()
