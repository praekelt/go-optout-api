import yaml

from twisted.internet.defer import inlineCallbacks
from twisted.web.server import Site

from vumi.tests.helpers import VumiTestCase

from go_optouts.server import HealthResource, read_yaml_config, ApiSite
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

    @inlineCallbacks
    def setUp(self):
        self.api_site = ApiSite()
        self.site_helper = yield self.add_helper(
            SiteHelper(self.api_site.site))

    @inlineCallbacks
    def test_health(self):
        result = yield self.site_helper.get('/health')
        self.assertEqual(result.code, 200)
        body = yield result.text()
        self.assertEqual(body, "OK")

    @inlineCallbacks
    def test_opt_out(self):
        result = yield self.site_helper.get('/optouts/count', headers={
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
