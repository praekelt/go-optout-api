"""
Tests for IOptOutStore.
"""
from opt_out_http_api.store.memory import OptOutMemory
from twisted.trial.unittest import TestCase
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks


class TestMemory(TestCase):
    def test_setup(self):
        store = OptOutMemory()
        assert store is not None
