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

import logging
import pygame

"""
Handles image display

Image display via pygame
"""
class PgImage(object):
    def __init__(self):
        self._screen = self._bg_surface =  None

        self._reset_screen()

    def __del__(self):
        pygame.display.quit()

    def _reset_screen(self):
        if pygame.display.get_init():
            pygame.display.quit()

        pygame.display.init()
        pygame.mouse.set_visible(False)
        self._width = pygame.display.Info().current_w
        self._height = pygame.display.Info().current_h
        self._screen = pygame.display.set_mode((self._width, self._height), pygame.FULLSCREEN)

    """
    Shows image

    :param mediafile: image to show
    """
    def play(self, imagefile):
        # Let's track media name for caller
        self.image = imagefile
        imgsurf = pygame.image.load(imagefile)

        # Check if image fits in display
        if imgsurf.get_width() > self._width or imgsurf.get_height() > self._height:
            # Rescale is needed
            imgsurf = pygame.transform.scale(imgsurf, (self._width, self._height))

        offsetX = (self._width - imgsurf.get_width()) / 2
        offsetY = (self._height - imgsurf.get_height()) / 2

        # Draw background if any
        if self._bg_surface:
            self._screen.blit(self._bg_surface, (0,0))
        self._screen.blit(imgsurf, (offsetX, offsetY))
        pygame.display.flip()

    def background(self, strhex):
        self._bg_surface =  pygame.Surface((self._width, self._height))

        if not (strhex == "#000000"):
            self._bg_surface.fill(pygame.Color(strhex))

        self._screen.blit(self._bg_surface, (0,0))
        pygame.display.flip()


