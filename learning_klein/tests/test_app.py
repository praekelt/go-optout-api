
from learning_klein.app import App
import treq
from twisted.trial.unittest import TestCase
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

class TestApp(TestCase):
    @inlineCallbacks
    def setUp(self):
        yield self.start_server()

    @inlineCallbacks
    def tearDown(self):
        yield self.stop_server()

    @inlineCallbacks
    def start_server(self):
        app = App()
        self.server = yield reactor.listenTCP(0, Site(app.app.resource()))
        addr = self.server.getHost()
        self.url = "http://%s:%s" % (addr.host, addr.port)

    @inlineCallbacks
    def stop_server(self):
        yield self.server.loseConnection()
# Tests
    @inlineCallbacks
    def test_hello(self):
        resp = yield treq.get("%s/Hello" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "Hello, world!")

    @inlineCallbacks
    def test_ar(self):
        resp = yield treq.get("%s/AR" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "I am the root page!")

    @inlineCallbacks
    def test_vr(self):
        resp = yield treq.get("%s/VR/Trevor" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "Hi Trevor!")

    @inlineCallbacks
    def test_rom(self):
        resp = yield treq.get("%s/ROM/bob" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "Hello there bob!")

    @inlineCallbacks
    def test_item(self):
        resp = yield treq.get("%s/infor/Contact" % (self.url,), persistent=False)
        data = yield resp.json()
        expected = [
        {"msg": "Hello", "Cell_No": 712345678, "Email": "trev@gmail.com"},
        {"msg": "Hello2", "Cell_No": 849485738, "Email": "oct@gmail.com"}
        ]
        self.assertEqual(data, expected)