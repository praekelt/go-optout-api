""" Test for the Riak opt out backend. """

from twisted.internet.defer import inlineCallbacks, returnValue
from zope.interface.verify import verifyClass, verifyObject

from vumi.tests.helpers import VumiTestCase
from vumi.tests.helpers import PersistenceHelper

from go.vumitools.opt_out.models import OptOutStore

from opt_out_http_api.store.interface import IOptOutStore
from opt_out_http_api.store.riak import (
    RiakOptOutBackend, RiakOptOutCollection)


class TestRiakOptOutBackend(VumiTestCase):
    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    @inlineCallbacks
    def mk_backend(self):
        manager = yield self.persistence_helper.get_riak_manager()
        backend = RiakOptOutBackend(manager)
        returnValue(backend)

    @inlineCallbacks
    def test_get_opt_out_collection(self):
        backend = yield self.mk_backend()
        collection = backend.get_opt_out_collection("owner-1")
        self.assertEqual(collection.store.user_account_key, "owner-1")
        self.assertTrue(isinstance(collection, RiakOptOutCollection))


class TestRiakOptOutCollection(VumiTestCase):
    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    @inlineCallbacks
    def mk_collection(self, owner_id):
        manager = yield self.persistence_helper.get_riak_manager()
        store = OptOutStore(manager, owner_id)
        collection = RiakOptOutCollection(store)
        returnValue((store, collection))

    def test_class_iface(self):
        self.assertTrue(verifyClass(IOptOutStore, RiakOptOutCollection))

    @inlineCallbacks
    def test_instance_iface(self):
        _store, collection = yield self.mk_collection("owner-1")
        self.assertTrue(verifyObject(IOptOutStore, collection))

    @inlineCallbacks
    def test_get_opt_out_exists(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out_1 = yield store.new_opt_out(
            "msisdn", "+12345", {"message_id": "FIXME"})
        opt_out_2 = yield collection.get("msisdn", "+12345")
        self.assertEqual(opt_out_2, {
            'created_at': opt_out_1.get_data().get('created_at'),
            'message': u'FIXME',
            'user_account': u'owner-1',
        })

    @inlineCallbacks
    def test_get_opt_out_absent(self):
        store, collection = yield self.mk_collection("owner-1")
        opt_out = yield collection.get("msisdn", "+12345")
        self.assertEqual(opt_out, None)
