import yaml

from twisted.internet.defer import inlineCallbacks
from twisted.web.server import Site

from vumi.tests.helpers import VumiTestCase, PersistenceHelper

from go_optouts.server import HealthResource, read_yaml_config, ApiSite
from go_optouts.store.memory import MemoryOptOutBackend
from go_optouts.store.riak import RiakOptOutBackend
from go_optouts.tests.utils import SiteHelper


class TestHealthResource(VumiTestCase):

    @inlineCallbacks
    def setUp(self):
        self.site = Site(HealthResource())
        self.site_helper = yield self.add_helper(SiteHelper(self.site))

    @inlineCallbacks
    def test_health_resource(self):
        result = yield self.site_helper.get('/')
        self.assertEqual(result.code, 200)
        body = yield result.text()
        self.assertEqual(body, "OK")


class TestReadYamlConfig(VumiTestCase):

    def mk_config(self, data):
        path = self.mktemp()
        with open(path, "wb") as f:
            f.write(yaml.safe_dump(data))
        return path

    def test_read_config(self):
        path = self.mk_config({
            "foo": "bar",
        })
        data = read_yaml_config(path)
        self.assertEqual(data, {
            "foo": "bar",
        })

    def test_optional_config(self):
        data = read_yaml_config(None)
        self.assertEqual(data, {})


class TestApiSite(VumiTestCase):

    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    def mk_config(self, data):
        path = self.mktemp()
        with open(path, "wb") as f:
            f.write(yaml.safe_dump(data))
        return path

    def mk_api_site(self, config=None):
        if config is None:
            config = {}
        if "backend" not in config:
            config["backend"] = "memory"
        return ApiSite(self.mk_config(config))

    def mk_server(self, config=None):
        api_site = self.mk_api_site(config)
        return self.add_helper(
            SiteHelper(api_site.site))

    @inlineCallbacks
    def test_health(self):
        site_helper = yield self.mk_server()
        result = yield site_helper.get('/health')
        self.assertEqual(result.code, 200)
        body = yield result.text()
        self.assertEqual(body, "OK")

    @inlineCallbacks
    def test_opt_out(self):
        site_helper = yield self.mk_server()
        result = yield site_helper.get('/optouts/count', headers={
            "X-Owner-ID": "owner-1",
        })
        self.assertEqual(result.code, 200)
        data = yield result.json()
        self.assertEqual(data, {
            'opt_out_count': 0,
            'status': {
                'code': 200,
                'reason': 'OK',
            },
        })

    @inlineCallbacks
    def test_url_path_prefix(self):
        site_helper = yield self.mk_server({
            "url_path_prefix": "wombats"
        })
        result = yield site_helper.get('/wombats/count', headers={
            "X-Owner-ID": "owner-1",
        })
        self.assertEqual(result.code, 200)
        data = yield result.json()
        self.assertEqual(data, {
            'opt_out_count': 0,
            'status': {
                'code': 200,
                'reason': 'OK',
            },
        })

    def test_memory_backend(self):
        api_site = self.mk_api_site({"backend": "memory"})
        backend = api_site.backend
        self.assertTrue(isinstance(backend, MemoryOptOutBackend))

    def test_riak_backend(self):
        config = self.persistence_helper.mk_config({})['riak_manager']
        api_site = self.mk_api_site({
            "backend": "riak",
            "backend_config": config,
        })
        backend = api_site.backend
        self.assertTrue(isinstance(backend, RiakOptOutBackend))
        self.assertEqual(
            backend.riak_manager.bucket_prefix, config["bucket_prefix"])
