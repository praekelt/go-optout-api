import json
from learning_klein.app import app
 
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
        self.server = yield reactor.listenTCP(0, Site(app.resource()))
        addr = self.server.getHost()
        self.url = "http://%s:%s" % (addr.host, addr.port)
 
    @inlineCallbacks
    def stop_server(self):
        yield self.server.loseConnection()
#---------------------------------------------Test--------------------------------------------------------- 
    
    @inlineCallbacks
    def get_item(self):
        resp = yield treq.get("%s/get_item/info" % (self.url,), persistent=False)
        content = yield resp.content()
        #expected = ;
        self.assertEqual(content, "{Contact:[{msg:\"Hello world1!\", Cell_No:27712345678, Email: \"trevor@gmail.com\"},{msg:\"Hello world is done\", Cell_No:27849485738, Email: \"october@gmail.com\"}]}")