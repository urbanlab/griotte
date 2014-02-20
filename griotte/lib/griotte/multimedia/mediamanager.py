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
    @staticmethod
    """
    Get available videos in the store
    :rtype: string -- JSON array of videos containing name:, type: and thumbnail: keys
    """
    def getVideos():
        return MediaManager._get('video')

    @staticmethod
    """
    Get available audio clips in the store
    :rtype: string -- JSON array of clips containing name:, type: and thumbnail: keys
    """
    def getAudios():
        return MediaManager._get('audio')

    @staticmethod
    """
    Get available images in the store
    :rtype: string -- JSON array of images containing name:, type: and thumbnail: keys
    """
    def getImages():
        return MediaManager._get('image')

    @staticmethod
    """
    Get available scenarios in the store
    :rtype: string -- JSON array of scenarios containing name:, type: and thumbnail: keys
    """
    def getScenarios():
        return MediaManager._get('scenario')

    @staticmethod
    """
    Get all available medias in the store
    :rtype: string -- JSON dict of media arrays keyed by type ('video', 'audio', 'image', 'scenario'). Each array item contains name:, type: and thumbnail: keys
    """
    def getMedias():
        result = {}
        for k in ['video', 'audio', 'image', 'scenario']:
            result[k] = MediaManager._get(k)

        return result
        #json.dumps(result)

    @staticmethod
    """
    Gets information on specific media
    :rtype: string -- JSON dict of metadata  with name:, type: and thumbnail: keys
    """
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
        response = { 'name': file,
                     'type': genre,
                     'thumbnail':"/store/%s/%s_thumbnail.jpg" % (genre, file) }

        if genre in ['audio', 'scenario']:
            response['thumbnail'] = "/img/%s_thumbnail.png" % genre

        meta = "%s/%s/%s_meta.json" % (options.medias, genre, file)
        if os.path.isfile(meta):
            logging.info("reading metadata for %s from %s" % (file, meta))

            with open(meta) as data_file:
                response.update(json.load(data_file))
        else:
            response['note'] = "No metadata found"

        return response
