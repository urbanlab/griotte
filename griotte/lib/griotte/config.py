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
import logging
import configparser
import os

"""
Sensible defaults for module
"""

class Config:
    def __init__(self, section):
        self._config = configparser.ConfigParser()
        self._section = section

        # Potential config files
        LOCATIONS = [ '/etc/griotte.ini',
                      '/usr/local/etc/griotte.ini',
                      'griotte/config/griotte.ini', # for checkouts
                      os.path.expanduser("~") + '/.griotte.ini' ]

        for file in LOCATIONS:
            if os.path.exists(file):
                logging.info("reading config file %s" % file)
                self._config.read_file(open(file))
                # First file wins
                break;

        self._translate_to_tornado()
        options.parse_command_line()

    def __getitem__(self, name):
        if name in self._config:
            return self._config[name]

    def __iter__(self):
        return iter(self._config)

    def _translate_to_tornado(self):
        if self._config is None:
            return

        try:
            for key in self._config[self._section]:
                # If this key doesn't exist for tornado, we make it
                if not key in options._options:
                    if key in ['default_port', 'server_port']:
                        define(key, default=int(self._config[self._section][key]), type=int)
                    else:
                        define(key, default=self._config[self._section][key])

                # Set the value in tornado option
                opt = options._options[key]
                opt.parse(self._config[self._section][key])

        except KeyError:
            logging.error("unable to find keys for section %s" % self._section)
            exit(0)





