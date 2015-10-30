import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web import http
from twisted.web.resource import Resource

from vumi.utils import build_web_site

import yaml

from .api import API
from .store.memory import MemoryOptOutBackend


class HealthResource(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setResponseCode(http.OK)
        request.do_not_log = True
        return 'OK'


def read_yaml_config(config_file, optional=True):
    """Parse an (usually) optional YAML config file."""
    if optional and config_file is None:
        return {}
    with file(config_file, 'r') as stream:
        # Assume we get a dict out of this.
        return yaml.safe_load(stream)


class ApiSite(object):
    """ Site for serving the opt out API. """

    def __init__(self, config_file=None):
        self.config = read_yaml_config(config_file)
        self.backend = self._backend_from_config(self.config)
        self.api = API(self.backend)
        url_path_prefix = self._url_path_prefix_from_config(self.config)
        self.site = build_web_site({
            'health': HealthResource(),
            url_path_prefix: self.api.app.resource(),
        })

    def _backend_from_config(self, config):
        return MemoryOptOutBackend()

    def _url_path_prefix_from_config(self, config):
        prefix = config.get('url_path_prefix')
        return prefix or "optouts"

    def run(self, host, port):
        log.startLogging(sys.stdout)
        reactor.listenTCP(port, self.site, interface=host)
        reactor.run()


if __name__ == "__main__":
    site = ApiSite()
    site.run('localhost', 8080)
