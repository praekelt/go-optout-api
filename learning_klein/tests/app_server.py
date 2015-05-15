
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
#---------------------------------------------Test--------------------------------------------------------- 
    @inlineCallbacks
    def test_Hello(self):
        resp = yield treq.get("%s/Hello" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "Hello, world!")

    @inlineCallbacks
    def test_AR(self):
        resp = yield treq.get("%s/AR" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "I am the root page!")

    @inlineCallbacks
    def test_VR(self):
        resp = yield treq.get("%s/VR/Trevor" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "Hi Trevor!")

    @inlineCallbacks
    def test_ROM(self):
        resp = yield treq.get("%s/ROM/bob" % (self.url,), persistent=False)
        content = yield resp.content()
        self.assertEqual(content, "Hello there bob!")

    @inlineCallbacks
    def test_item(self):
        resp = yield treq.get("%s/infor/Contact" % (self.url,), persistent=False)
        data = yield resp.json()
        expected = [{"msg":"Hello world!", "Cell_No":27712345678, "Email": "trevor@gmail.com"},
        {"msg":"Hello world is done", "Cell_No":27849485738, "Email": "october@gmail.com"}]
        self.assertEqual(data, expected)