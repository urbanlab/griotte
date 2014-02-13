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
import json
import os
import fnmatch

from tornado.options import options

"""

"""
class MediaManager:
    @staticmethod
    def getVideos():
        return MediaManager._get('video')

    @staticmethod
    def getAudios():
        return MediaManager._get('audio')

    @staticmethod
    def getImages():
        return MediaManager._get('image')

    @staticmethod
    def getMedias():
        result = {}
        for k in ['video', 'audio', 'image']:
            result[k] = MediaManager._get(k)

        return result
        #json.dumps(result)

    @staticmethod
    def get(target):
        return json.dumps(MediaManager._get(target))

    @staticmethod
    def _get(target):
        response = []
        for file in os.listdir("%s/%s" % (options.medias, target)):
            if not fnmatch.fnmatch(file, '*_thumbnail.jpg') and not fnmatch.fnmatch(file, '*_meta.json'):
                response.append(MediaManager._build_response_for(file, target))

        return response

    @staticmethod
    def _build_response_for(file, genre):
        response = { 'name': file, 'type': genre, 'thumbnail':"/store/%s/%s_thumbnail.jpg" % (genre, file) }
        if genre == 'audio':
            response['thumbnail'] = "/img/audio_thumbnail.png"

        meta = "%s/%s/%s_meta.json" % (options.store, genre, file)
        if os.path.isfile(meta):
            logging.info("reading metadata for %s from %s" % (file, meta))

            with open(meta) as data_file:
                response.update(json.load(data_file))
        else:
            response['note'] = "No metadata found"

        return response
