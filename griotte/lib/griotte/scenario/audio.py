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

"""Server-side Audio groups blocks implementation

This module implements server-side code generated for audio blockly blocks.

.. module:: audio
   :platform: Unix

.. moduleauthor:: Michel Blanc <mblanc@erasme.org>

"""


def play_audio(media, sync=True):
    """ Plays sound synchronously

    Plays sound and wait for completion

    :param media: The media to play, relative to the media root folder
    """
    Expecter().send('audio.command.start', { "media": media })
    if sync:
        Expecter().expect('audio.event.stop')
