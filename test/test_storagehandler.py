# Tests for websockets

import unittest
import tempfile

from griotte.storage.storagehandler import StorageHandler

STORAGE=tempfile.mkstemp()[1]

class Mock:
    def __init__(self, *args):
        self.called = {}
        for item in args:
            self.called[item] = { 'times': 0, 'args' : [] }

        from pprint import pprint
        pprint(self.called)

    def send(self, *args):
        self.called['send']['times'] += 1
        self.called['send']['args'] += args
        return

    def add_listener(self, *args):
        self.called['add_listener'] += 1
        return

    def times(self, member):
        return self.called[member]['times']

    def args(self, member):
        return self.called[member]['args']

    def stop(self):
        return

def mock_storage(target = None):
        if target:
            target._ws.stop()

        sh = StorageHandler(STORAGE)
        sh._ws = Mock('send', 'add_listener')
        return sh

class StorageHandlerTests(unittest.TestCase):
    def setUp(self):
        self.store = mock_storage()
        self.store._ws = Mock('send', 'add_listener')

    def tearDown(self):
        self.store.stop()

    # def testListeners(self):
    #     self.assertEqual(self.store._ws.called['add_listener'], 2)

    def testGet(self):
        self.store.set("store.set.foo", { 'data' : 'baz' })
        self.store.get("store.set.foo", "")
        self.assertEqual(self.store._ws.times('send'), 1)
        self.assertEqual(self.store._ws.args('send'), ["store.event.foo", "baz"])

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

        self.store = mock_storage(self.store)
        self.assertEqual(self.store._store['foo'], 'fizz')

    def testSetDeepPersistent(self):
        self.store.set("store.set.foo",
                       { 'data' : {'bar': { 'fizz' : 'fuzz' }},
                        'persistent': True})

        self.store = mock_storage(self.store)
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'fuzz')

if __name__ == "__main__":
    unittest.main()

