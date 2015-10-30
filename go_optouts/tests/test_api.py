from go_optouts.api_methods import API
import treq
from twisted.trial.unittest import TestCase
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from go_optouts.store.memory import OptOutMemory


class TestApi(TestCase):
    @inlineCallbacks
    def setUp(self):
        yield self.start_server()

    @inlineCallbacks
    def tearDown(self):
        yield self.stop_server()

    @inlineCallbacks
    def start_server(self):
        self.backend = OptOutMemory()
        self.app = API(self.backend)
        self.server = yield reactor.listenTCP(0, Site(self.app.app.resource()))
        addr = self.server.getHost()
        self.url = "http://%s:%s" % (addr.host, addr.port)

    @inlineCallbacks
    def stop_server(self):
        yield self.server.loseConnection()

    def api_call(self, path):
        return treq.get("%s%s" % (self.url, path), persistent=False)

    def api_put(self, path):
        return treq.put("%s%s" % (self.url, path), persistent=False)

    def api_delete(self, path):
        return treq.delete("%s%s" % (self.url, path), persistent=False)

    def api_count(self, path):
        return treq.get("%s%s" % (self.url, path), persistent=False)


# Tests

    @inlineCallbacks
    def test_opt_out_found(self):
        existing_opt_out = self.backend.put("msisdn", "+273121100")
        resp = yield self.api_call("/optouts/msisdn/+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": existing_opt_out["id"],
                "address_type": "msisdn",
                "address": "+273121100",
            },
        })

    @inlineCallbacks
    def test_opt_out_not_found(self):
        resp = yield self.api_call("/optouts/mxit/+369963")
        self.assertEqual(resp.code, 404)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 404,
                "reason": "Opt out not found.",
            },
        })

    @inlineCallbacks
    def test_opt_out_created(self):
        resp = yield self.api_put("/optouts/msisdn/+273121100")
        created_opt_out = self.backend.get("msisdn", "+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": created_opt_out["id"],
                "address_type": "msisdn",
                "address": "+273121100"
            },
        })

    @inlineCallbacks
    def test_opt_out_conflict(self):
        self.backend.put("msisdn", "+273121100")
        response = yield self.api_put("/optouts/msisdn/+273121100")
        self.assertEqual(response.code, 409)
        data = yield response.json()
        self.assertEqual(data, {
            "status": {
                "code": 409,
                "reason": "Opt out already exists."
            },
        })

    @inlineCallbacks
    def test_opt_out_deleted(self):
        delete_opt_out = self.backend.put("whatsapp", "@whatsup")
        resp = yield self.api_delete("/optouts/whatsapp/@whatsup")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": delete_opt_out["id"],
                "address_type": "whatsapp",
                "address": "@whatsup"
            },
        })

    @inlineCallbacks
    def test_opt_out_nothing_to_delete(self):
        response = yield self.api_delete("/optouts/whatsapp/+2716230199")
        self.assertEqual(response.code, 404)
        data = yield response.json()
        self.assertEqual(data, {
            "status": {
                "code": 404,
                "reason": "There\'s nothing to delete."
            },
        })

    @inlineCallbacks
    def test_opt_out_count_zero_opt_out(self):
        resp = yield self.api_count("/optouts/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 0,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })

    @inlineCallbacks
    def test_opt_out_count_two_opt_outs(self):
        self.backend.put("slack", "@slack")
        self.backend.put("twitter_handle", "@trevor_october")
        resp = yield self.api_count("/optouts/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 2,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })

    @inlineCallbacks
    def test_opt_out_count_three_opt_outs(self):
        self.backend.put("whatsapp", "+27782635432")
        self.backend.put("mxit", "@trevor_mxit")
        self.backend.put("facebook", "fb")
        resp = yield self.api_count("/optouts/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 3,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })
