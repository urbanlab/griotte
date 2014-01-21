#
# (c) 2013-2014 ERASME
#
# This file is part of Griotte
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
# along with Griotte.  If not, see <http://www.gnu.org/licenses/>.

import signal
import sys

def signal_handler(signal, frame):
        print('Exiting')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
