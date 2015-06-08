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

    def api_call(self, path):
        return treq.get("%s%s" % (self.url, path), persistent=False)

# Tests

    @inlineCallbacks
    def test_opt_out_found(self):
        resp = yield self.api_call("/optouts/msisdn/+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "id": "2468",
            "address_type": "msisdn",
            "address": "+273121100",
        })
