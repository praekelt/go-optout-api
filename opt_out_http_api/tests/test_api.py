from opt_out_http_api.api_methods import API
import treq
from twisted.trial.unittest import TestCase
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks


class TestApi(TestCase):
    @inlineCallbacks
    def setUp(self):
        yield self.start_server()

    @inlineCallbacks
    def tearDown(self):
        yield self.stop_server()

    @inlineCallbacks
    def start_server(self):
        app = API()
        self.server = yield reactor.listenTCP(0, Site(app.app.resource()))
        addr = self.server.getHost()
        self.url = "http://%s:%s" % (addr.host, addr.port)

    @inlineCallbacks
    def stop_server(self):
        yield self.server.loseConnection()
# Tests

    @inlineCallbacks
    def test_address(self):
        resp = yield treq.get("%s/optouts/addresses" % (self.url,), persistent=False)
        data = yield resp.json()
        expected = [
            {"id": "2468", "address_type": "msisdn", "address": "+273121100"},
            {"id": "1234", "address_type": "facebook", "address": "fb-app"},
            {"id": "5678", "address_type": "twitter", "address": "@twitter_handle"}
        ]
        self.assertEqual(data, expected)
