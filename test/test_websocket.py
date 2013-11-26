# Tests for websockets

import unittest
import socket

from raspeomix.websocket import WebSocket

class WebSocketTests(unittest.TestCase):

    def testInit(self):
        ws = WebSocket()
        self.failUnless(ws.prefix == socket.gethostname())

if __name__ == "__main__":
    unittest.main()

