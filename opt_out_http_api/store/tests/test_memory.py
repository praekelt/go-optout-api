"""
Tests for IOptOutStore.
"""
from zope.interface.verify import verifyClass, verifyObject
from opt_out_http_api.store.interface import IOptOutStore
from opt_out_http_api.store.memory import OptOutMemory
from twisted.trial.unittest import TestCase


class TestMemory(TestCase):
    def test_setup_class_iface(self):
        self.assertTrue(verifyClass(IOptOutStore, OptOutMemory))

    def test_setup_instance_iface(self):
        self.assertTrue(verifyObject(IOptOutStore, OptOutMemory()))

    def test_put_and_get(self):
        store = OptOutMemory()
        opt1 = store.put("twitter_handle", "@trevor")
        self.assertEqual(len(opt1["id"]), 36)  # length of uuid-4 string
        self.assertEqual(opt1, {
            "id": opt1["id"],
            "address_type": "twitter_handle",
            "address": "@trevor"
        })
        opt2 = store.get("twitter_handle", "@trevor")
        self.assertEqual(opt2, {
            "id": opt1["id"],
            "address_type": "twitter_handle",
            "address": "@trevor"
        })
