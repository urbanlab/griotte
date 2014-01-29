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

    def send(self, *args):
        self.called['send']['times'] += 1
        self.called['send']['args'] += args
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
        sh._ws = Mock('send')
        return sh

class StorageHandlerTests(unittest.TestCase):
    def setUp(self):
        self.store = mock_storage()

    def tearDown(self):
        self.store.stop()

    def testGet(self):
        self.store.set("store.command.set.foo", { 'value' : 'baz' })
        self.store.get("store.command.set.foo", "")
        self.assertEqual(self.store._ws.times('send'), 1)
        self.assertEqual(self.store._ws.args('send'), ["store.event.foo", { 'value' : 'baz' } ])

    def testGetComplex(self):
        self.store.set("store.command.set.foo.fizz", { 'value' : 'buz' })
        self.store.get("store.command.set.foo", "")
        self.assertEqual(self.store._ws.times('send'), 1)
        self.assertEqual(self.store._ws.args('send'), ["store.event.foo",{ 'value' : { 'fizz' : 'buz' }} ])

    def testSet(self):
        self.store.set("store.command.set.foo", { 'value' : 'baz' })
        self.assertEqual(self.store._store['foo'], 'baz')

    def testSetNested(self):
        self.store.set("store.command.set.foo", { 'value' : {'bar': { 'fizz' : 'fuzz' }}})
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'fuzz')

    def testSetDeep(self):
        self.store.set("store.command.set.foo.bar.fizz", { 'value' : 'deep' })
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'deep')

    def testSetMerges(self):
        self.store.set("store.command.set.foo.bar.fizz", { 'value' : 'deep' })
        self.store.set("store.command.set.foo.bar.fuzz", { 'value' : 'bizz' })
        self.store.set("store.command.set.foo.bar", { 'value' : { 'fizz' : 'overriden' }})
        self.store.set("store.command.set.foo.bar.baz", { 'value' : 'baz' })
        from pprint import pprint
        pprint(self.store._store)
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'overriden')
        self.assertEqual(self.store._store['foo']['bar']['fuzz'], 'bizz')
        self.assertEqual(self.store._store['foo']['bar']['baz'], 'baz')

    def testSetPersistent(self):
        self.store.set("store.command.set.foo",
                       {'value': 'fizz',
                        'persistent': True})

        self.store = mock_storage(self.store)
        self.assertEqual(self.store._store['foo'], 'fizz')

    def testSetNestedPersistent(self):
        self.store.set("store.command.set.foo",
                       { 'value' : {'bar': { 'fizz' : 'fuzz' }},
                        'persistent': True})

        self.store = mock_storage(self.store)
        self.assertEqual(self.store._store['foo']['bar']['fizz'], 'fuzz')

    def testEmptyStorage(self):
        self.store = StorageHandler()
        self.store._ws = Mock('send')
        self.assertEqual(self.store._store, {})

    def testWrongMessage(self):
        self.store = StorageHandler()
        # The first should not raise, but catch and log the error
        self.store.set("store.command.set.foo", { 'omg_wrong_key' : 'deep' })
        with self.assertRaises(KeyError):
            # But this one should raise
            self.store._store['foo']

if __name__ == "__main__":
    unittest.main()

