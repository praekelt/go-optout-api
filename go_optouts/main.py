""" Command for launching the Vumi Go Opt Out API. """

import click

from .server import ApiSite


@click.command()
@click.version_option()
@click.option('--config', '-c', help='YAML config file')
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', type=int, default=8080)
def run(config, host, port):
    """ Vumi Go Opt Out API. """
    site = ApiSite(config)
    site.run(host, port)
