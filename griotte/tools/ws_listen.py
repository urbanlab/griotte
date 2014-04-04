#!/usr/bin/env python3

# Usage :
# tools/ws_listen.py --watchdog=2 --logging=debug some:channel some:other:channel

import json
import sys
import logging
from tornado.options import define, options

from griotte.ws import WebSocket
from griotte.config import Config
import tornado.ioloop

Config("DEFAULT")

define("watchdog", default=0, help="Watchdog interval")

if __name__ == "__main__":
    def on_message(channel, message):
        logging.info(" >>> On channel \"%s\" : %s" % (channel, message))

    channels = ()
    channels = options.parse_command_line()

    if not channels:
        logging.warning("No channel specified, watching meta.presence")
        channels.append("meta.presence")

    ws = WebSocket(watchdog_interval=options.watchdog)
    for chan in channels:
        ws.add_listener(chan, on_message)

    ws.start(detach=False)
    tornado.ioloop.IOLoop.instance().start()

