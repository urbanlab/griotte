# Tests for websockets

import unittest
import socket

from griotte.ws import WebSocket

class WebSocketTests(unittest.TestCase):

    def testInit(self):
        ws = WebSocket()
        self.assertTrue(ws.prefix == socket.gethostname())

if __name__ == "__main__":
    unittest.main()

