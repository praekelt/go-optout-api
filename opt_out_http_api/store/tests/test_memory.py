"""
Tests for IOptOutStore.
"""
from zope.interface.verify import verifyClass, verifyObject
from opt_out_http_api.store.interface import IOptOutStore
from opt_out_http_api.store.memory import OptOutMemory
from twisted.trial.unittest import TestCase


class TestMemory(TestCase):
    def test_setup(self):
        store = OptOutMemory()
        assert verifyObject(IOptOutStore, store)

    def test_setup_class_iface(self):
        assert verifyClass(IOptOutStore, OptOutMemory)

    def test_setup_instance_iface(self):
        assert verifyObject(IOptOutStore, OptOutMemory())

    def test_get(self):
        store = OptOutMemory()
        assert (IOptOutStore.get, store)
