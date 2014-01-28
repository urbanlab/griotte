#
# (c) 2013-2014 ERASME
#
# This file is part of Raspeomix
#
# Raspeomix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Raspeomix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Raspeomix.  If not, see <http://www.gnu.org/licenses/>.

#
# Defaults
#

from tornado.options import define, options
import os

"""
Sensible defaults for module
"""

try:
    define("default-server",
           default="127.0.0.1",
           help="Default server to use for websocket client connections")

    define("default-port",
           default=8888,
           type=int,
           help="Default port to use for websocket client connections")

    define("server-port",
           default=8888,
           type=int,
           help="Port to use for web and websocket server")

    define("document-root",
           default="/usr/local/share/griotte/static",
           help="Root for static web files served by the internal webserver")

    define("store",
           default="/usr/local/share/griotte/store",
           help="Storage directory for storage module")

    define("medias",
           default="/medias",
           help="Directory containing medias")

    # Potential config files
    LOCATIONS = [ '/etc/griotte.conf',
                  '/usr/local/etc/griotte.conf',
                  'griotte/config/griotte.conf', # for checkouts
                  os.path.expanduser("~") + '/.griotte.conf' ]

    for file in LOCATIONS:
        if os.path.exists(file):
            options.parse_config_file(file, final=False)

    options.parse_command_line()
except:
    pass
