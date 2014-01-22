"""Storage module

This module handle storing and yielding data.
It can store whatever is send on the wire in the store channel.

The message format is documented in :doc:`messages`.


.. moduleauthor:: Michel Blanc <mblanc@erasme.org>
.. versionadded:: 0.0.1

Test me with :

.. code-block:: bash

    griotte/tools/ws_send.py store.set.wtf '{ "value" : { "a": { "b": "z" } }, "persistent": true }'

"""

import logging
import json
import tempfile
import sys

from tornado.options import options

from griotte.ws import WebSocket
from griotte.utils import dict_merge

class StorageHandler:
    """ Storage handling class

    Store and sends values over websockets
    """

    def __init__(self, store="%s/store.json" % options.store):
        logging.debug("Starting StorageHandler")

        self._store_path = store
        self._store = self._thaw()

        self._ws = WebSocket(watchdog_interval=2)
        self._ws.add_listener('store.set.*', self.set)
        self._ws.add_listener('store.get.*', self.get)

        self.start()

    def get(self, channel, message):
        """ Callback for the get operation

        :param channel: The name of the channel containing the get request
        :type channel: str
        :param message: The message received over the channel
        :type message: dict -- not used
        """

        variable = self._get_struct(self._get_variable_from_channel(channel), self._store)

        return_channel = "store.event." + ".".join(self._get_variable_from_channel(channel))
        self._ws.send(return_channel, variable)

    def set(self, channel, data):
        """ Callback for the set operation

        Data, passed via a dict, can come in two flavors :
        * value : single valued data
        * { 'a' : { 'b' : 'c' } } : deep structure

        The later is the same as publishing 'c' in the
        `store.set.a.b` channel.

        :param channel: The name of the channel containing the set request
        :type channel: str
        :param message: The message received over the channel
        :type message: dict
        """

        if 'value' in data:
            nested = self._set_struct(self._get_variable_from_channel(channel),
                                      data['value'])
            self._store = dict_merge(self._store, nested)

            if 'persistent' in data:
                self._freeze(nested)
        else:
            logging.error("A client sent a message without a valid 'value' field")

    def start(self):
        logging.info("Starting StorageHandler's websocket")
        self._ws.start(detach=False)

    def stop(self):
        logging.info("Starting StorageHandler's websocket")
        self._ws.stop()

    def _get_struct(self, chanarr, value):
        """ Converts a channel and variable to a nested structure starting at
        root recursing over subkeys

        For instance, if { 'value' : 42 } is passed in channel
        `store.set.some.deep.structure`, `_get_struct` will return a dict :
        { 'some' : { 'deep' : { 'structure' : 42 }}}

        :param chanarr: Array containing subkeys
        :type chanarr: array
        :param value: Value received for the channel
        :type message: str
        """
        if len(chanarr) > 0:
            value = self._get_struct(chanarr[1:], value[chanarr[0]])

        return value

    def _set_struct(self, chanarr, variable):
        """ Converts a channel and variable to a nested structure starting at
        root recursing over subkeys

        For instance, if { 'value' : 42 } is passed in channel
        `store.set.some.deep.structure`, `_set_struct` will return a dict :
        { 'some' : { 'deep' : { 'structure' : 42 }}}

        :param chanarr: Array containing subkeys
        :type chanarr: array
        :param value: Value received for the channel
        :type message: str
        """

        value = {}
        if len(chanarr) != 0:
            value[chanarr[0]] = self._set_struct(chanarr[1:], variable)
        elif variable:
            value = variable

        return value

    def _get_variable_from_channel(self, channel):
        """ Converts channel name into a variable

        Extracted so it's easy to refactor if needed

        :rtype: array -- array of consecutive subkeys

        .. note:: may be this should be shared in griotte for other modules
        """
        return channel.split('.')[2:]

    def _thaw(self):
        """ Reads store from disk and returns it

        _thaw() doesn't write data directly to self.store. The caller must handle
        this.

        :rtype: Hash representing stored variables or an empty Hash of store
                file is not found
        """
        try:
            f = open(self._store_path, 'r')
        except FileNotFoundError:
            logging.warn("Unable to open store file '%s'. Starting empty.", self._store_path)
            return {}

        try:
            val = json.load(f)
        except ValueError:
            val = {}
            logging.error("Unable to parse json store file '%s'. Starting empty.", self._store_path)

        f.close()
        return val

    def _freeze(self, struct):
        """ Stores a specific variable in the startup store file

        :param variable: Key for variable to store
        :type variable: str
        """
        temp_data = self._thaw()
        temp_data = dict_merge(temp_data, struct)
        f = open(self._store_path, 'w')
        json.dump(temp_data, f)
        f.close()


