from opt_out_http_api.api_methods import API
import treq
import uuid
from twisted.trial.unittest import TestCase
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from opt_out_http_api.store.memory import OptOutMemory


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
        def fixed_uuid():
            return '36'
        self.patch(uuid, 'uuid4', fixed_uuid)
        resp = yield self.api_put("/optouts/msisdn/+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "36",
                "address_type": "msisdn",
                "address": "+273121100"
            },
        })

        resp = yield self.api_call("/optouts/msisdn/+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "36",
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
        def fixed_uuid():
            return '1234'
        self.patch(uuid, 'uuid4', fixed_uuid)
        resp = yield self.api_put("/optouts/linkedin/+1029384756")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "1234",
                "address_type": "linkedin",
                "address": "+1029384756"
            },
        })

    @inlineCallbacks
    def test_opt_out_conflict(self):
        def fixed_uuid():
            return '36'
        self.patch(uuid, 'uuid4', fixed_uuid)
        resp = yield self.api_put("/optouts/msisdn/+273121100")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "36",
                "address_type": "msisdn",
                "address": "+273121100"
            },
        })
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
        def fixed_uuid():
            return '2684'
        self.patch(uuid, 'uuid4', fixed_uuid)
        resp = yield self.api_put("/optouts/whatsup/@whatsup")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "2684",
                "address_type": "whatsup",
                "address": "@whatsup"
            },
        })
        resp = yield self.api_delete("/optouts/whatsup/@whatsup")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "2684",
                "address_type": "whatsup",
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
    def test_opt_out_count_two_opt_outs(self):
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
    def test_opt_out_count_three_opt_outs(self):
        def fixed_uuid():
            return '1010'
        self.patch(uuid, 'uuid4', fixed_uuid)
        resp = yield self.api_put("/optouts/msisdn/+271345")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "opt_out": {
                "id": "1010",
                "address_type": "msisdn",
                "address": "+271345"
            },
        })

        resp = yield self.api_count("/optouts/count")
        self.assertEqual(resp.code, 200)
        data = yield resp.json()
        self.assertEqual(data, {
            "opt_out_count": 1,
            "status": {
                "code": 200,
                "reason": "OK"
            },
        })
