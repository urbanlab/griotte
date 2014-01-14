"""Storage module

This module handle storing and yielding data.
It can store whatever is send on the wire in the store channel.

The message format is documented in :doc:`messages`.


.. moduleauthor:: Michel Blanc <mblanc@erasme.org>
.. versionadded:: 0.0.1
"""

import logging
import json
import tempfile
import griotte.constants as C
import sys

from griotte.ws import WebSocket

class StorageHandler:
    """ Storage handling class

    Store and sends values over websockets
    """

    def __init__(self, store=C.DEFAULT_STORE + '/store.json'):
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

        variable = self._get_variable(channel)
        value = None
        if variable in self._store:
            value = self._store[variable]

        self._ws.send("store.event." + variable, value)

    def set(self, channel, message):
        """ Callback for the set operation

        Data, passed via a dict, can come in two flavors :
        * { 'data': value } : single valued data
        * { 'data' : { 'a' : { 'b' : 'c' } } } : deep structure

        :param channel: The name of the channel containing the set request
        :type channel: str
        :param message: The message received over the channel
        :type message: dict
        """
        variable = self._get_variable(channel)
        # We need to check if it's a single value or a dict
        if isinstance(message["data"], dict):
            # Dict
            self._store[variable] = dict()
            for x in message["data"].keys():
                self._store[variable][x] = message["data"][x]
        else:
            # Single value
            self._store[variable] = message["data"]

        if 'persistent' in message:
            self._freeze(variable)

    def start(self):
        logging.info("Starting StorageHandler's websocket")
        self._ws.start()

    def stop(self):
        logging.info("Starting StorageHandler's websocket")
        self._ws.stop()

    def _get_variable(self, channel):
        """ Converts channel name into a variable

        Extracted so it's easy to refactor if needed

        :rtype: str

        .. note:: may be this should be shared in griotte for other modules
        """
        return ','.join(channel.split('.')[2:])

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
            logging.warn("Unable to open store file. Starting empty.")
            return {}

        try:
            val = json.load(f)
        except ValueError:
            val = {}
            logging.error("Unable to decode store file. Starting empty.")

        f.close()
        return val

    def _freeze(self, variable):
        """ Stores a specific variable in the startup store file

        :param variable: Key for variable to store
        :type variable: str
        """
        temp_data = self._thaw()
        temp_data[variable] = self._store[variable]
        f = open(self._store_path, 'w')
        json.dump(temp_data, f)
        f.close()


