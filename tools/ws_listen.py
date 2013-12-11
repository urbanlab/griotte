#!/usr/bin/env python3

# Usage :
# tools/ws_listen.py --watchdog=2 --logging=debug some:channel some:other:channel

import json
import sys
import logging
from tornado.options import define, options

from raspeomix.ws import WebSocket

define("url", default="ws://127.0.0.1:8888/ws", help="Websocket server url")
define("watchdog", default=0, help="Watchdog interval")
define("channels", default="meta:presence", multiple = True,
       help="Channels to watch (coma separated)")

if __name__ == "__main__":
    def on_message(message):
        print(message)

    channels = ()
    channels = options.parse_command_line()

    ws = WebSocket(watchdog_interval=options.watchdog)
    for chan in channels:
        ws.add_listener(chan, on_message)

    ws.start()

