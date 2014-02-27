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

# Volume icon (audio medias) by David Peters, EXBROOK, for Wikimedia Foundation
# http://commons.wikimedia.org/wiki/File:Volume-icon.gif
# CC-BY-SA-3.0

# Book icon (scenario medias) by David Peters, EXBROOK, for Wikimedia Foundation
# http://commons.wikimedia.org/wiki/File:Book-icon-orange.gif?uselang=fr
# CC-BY-SA-3.0

import logging
import json
import os
import fnmatch

from tornado.options import options

"""
MediaManager handles listing medias in the store
"""
class MediaManager:
    """
    Get all available medias in the store
    :rtype: string -- JSON dict of media arrays keyed by type ('video', 'audio', 'image', 'scenario'). Each array item contains name:, type: and thumbnail: keys
    """
    @staticmethod
    def get_all():
        result = {}
        for k in ['video', 'audio', 'image', 'scenario']:
            result[k] = MediaManager._get(k)

        return result
        #json.dumps(result)

    """
    Gets information on specific media
    :rtype: string -- JSON dict of metadata  with name:, type: and thumbnail: keys
    """
    @staticmethod
    def get(genre):
        return json.dumps(MediaManager._get(genre))

    """
    Gets information on specific media

    :param genre: type of media ('video', 'image', 'audio', 'scenario')
    :param name: media name
    :rtype: dict -- dict of metadata  with name:, type:, fullpath: and thumbnail: keys at least
    """
    @staticmethod
    def get_media_dict(genre, name):
        return MediaManager._build_response_for(genre, name)

    @staticmethod
    def _get(genre):
        response = []
        for f in os.listdir("%s/%s" % (options.store, genre)):
            if not fnmatch.fnmatch(f, '*_thumbnail.jpg') and not fnmatch.fnmatch(f, '*_meta.json'):
                response.append(MediaManager._build_response_for(genre, f))

        return response

    @staticmethod
    def _build_response_for(genre, name):
        response = { 'name': name,
                     'path': "%s/%s/%s" % (options.store, genre, name),
                     'type': genre,
                     'thumbnail':"/store/%s/%s_thumbnail.jpg" % (genre, name),
                     'thumbnail_square':"/store/%s/%s_square_thumbnail.jpg" % (genre, name),
                      }

        if genre in ['audio', 'scenario']:
            response['thumbnail'] = "/img/%s_thumbnail.png" % genre
            response['thumbnail_square'] = "/img/%s_thumbnail.png" % genre

        meta = "%s/%s/%s_meta.json" % (options.store, genre, name)
        if os.path.isfile(meta):
            logging.info("reading metadata for %s from %s" % (name, meta))

            with open(meta) as data_file:
                response.update(json.load(data_file))
        else:
            response['note'] = "No metadata found"

        return response
