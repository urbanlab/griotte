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
        self._shutdown()

    def _shutdown(self):
        logging.debug("pygame shutting down")
        pygame.display.quit()
        pygame.quit()

    def _reset_screen(self):
        pygame.display.quit()
        pygame.quit()
        if pygame.display.get_init():
            logging.debug("pygame.display.get_init")
            pygame.display.quit()

        logging.debug("pygame.display.init")
        pygame.display.init()
        logging.debug("pygame.mouse_set_visible")
        pygame.mouse.set_visible(False)
        self._width = pygame.display.Info().current_w
        self._height = pygame.display.Info().current_h
        logging.debug("pygame.set_mode")

        self._screen = pygame.display.set_mode((self._width, self._height), pygame.FULLSCREEN)

        logging.debug("pygame is ready")

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
            factor = max(imgsurf.get_width()/self._width, imgsurf.get_height()/self._height)

            imgsurf = pygame.transform.scale(imgsurf, (int(imgsurf.get_width() / factor), int(imgsurf.get_height()/factor)))

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


