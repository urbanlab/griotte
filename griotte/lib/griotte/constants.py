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
import os
import sys

"""
Sensible defaults for module
"""
DEFAULT_SERVER  = "127.0.0.1"
DEFAULT_PORT    = "8888"
DEFAULT_STATIC  = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                  '..', '..', '..', 'static'))

try:
    DEFAULT_STORE = os.environ['GRIOTTE_STORE']
except KeyError:
    print("No store defined. Please define the GRIOTTE_STORE environment variable.", file=sys.stderr)
    exit(1)

