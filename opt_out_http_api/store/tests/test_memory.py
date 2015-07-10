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
        opt3 = store.get("mxit", "praekelt_mxit")
        self.assertEqual(None, opt3)

    def test_delete_missing(self):
        store = OptOutMemory()
        opt_out_delete = store.delete("twitter_handle", "@trevor")
        self.assertEqual(None, opt_out_delete)

    def test_put_and_delete(self):
        store = OptOutMemory()
        opt_put = store.put("facebook", "trevor_fb")
        self.assertEqual(len(opt_put["id"]), 36)
        self.assertEqual(opt_put, {
            "id": opt_put["id"],
            "address_type": "facebook",
            "address": "trevor_fb"
        })

        opt_out_del = store.delete("facebook", "trevor_fb")
        self.assertEqual(opt_out_del, {
            "id": opt_put["id"],
            "address_type": "facebook",
            "address": "trevor_fb"
        })

        opt_out_get = store.get("facebook", "trevor_fb")
        self.assertEqual(opt_out_get, None)

    def test_count(self):
        store = OptOutMemory()
        opt_count = store.count()
        self.assertEqual(opt_count, 0)

        opt_put = store.put("wechat", "vumi")
        self.assertEqual(len(opt_put["id"]), 36)
        self.assertEqual(opt_put, {
            "id": opt_put["id"],
            "address_type": "wechat",
            "address": "vumi"
        })

        opt_count2 = store.count()
        self.assertEqual(opt_count2, 1)
