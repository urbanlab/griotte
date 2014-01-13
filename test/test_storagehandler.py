# Tests for websockets

import unittest
import tempfile

from griotte.storage.storagehandler import StorageHandler

STORAGE=tempfile.mkstemp()[1]

class Mock:
    def __init__(self):
        self.called = { 'send' : 0, 'add_listener': 0 }

    def send(self, *args):
        self.called['send'] += 1
        return

    def add_listener(self, *args):
        self.called['add_listener'] += 1
        return


class StorageHandlerTests(unittest.TestCase):
    def setUp(self):
        self.store = StorageHandler(STORAGE)
        self.store._ws = Mock()

    # def testListeners(self):
    #     self.assertEqual(self.store._ws.called['add_listener'], 2)

    def testGet(self):
        self.store.get("store.set.foo", "")
        self.assertEqual(self.store._ws.called['send'], 1)

    def testSet(self):
        self.store.set("store.set.foo", { 'data' : 'baz' })
        self.assertEqual(self.store._store['foo'], 'baz')

    def testSetDeep(self):
        self.store.set("store.set.foo", { 'data' : {'bar': { 'fizz' : 'fuzz' }}})
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'fuzz')

    def testSetPersistent(self):
        self.store.set("store.set.foo",
                       {'data': 'fizz',
                        'persistent': True})

        self.store = StorageHandler(STORAGE)
        self.assertEqual(self.store._store['foo'], 'fizz')

    def testSetDeepPersistent(self):
        self.store.set("store.set.foo",
                       { 'data' : {'bar': { 'fizz' : 'fuzz' }},
                        'persistent': True})

        self.store = StorageHandler(STORAGE)
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'fuzz')

if __name__ == "__main__":
    unittest.main()

