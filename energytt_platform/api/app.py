import flask
import logging
from typing import List
from functools import cached_property

from .endpoints import Endpoint
from .guards import EndpointGuard
from .requests import GetHandler, PostHandler


class Application(object):
    """
    TODO
    """
    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.debug = debug

    @cached_property
    def _flask_app(self) -> flask.Flask:
        """
        TODO
        """
        app = flask.Flask(self.name)
        if self.debug:
            app.logger.setLevel(logging.DEBUG)
        return app

    @property
    def wsgi_app(self) -> flask.Flask:
        """
        TODO
        """
        return self._flask_app

    def add_endpoint(
            self,
            method: str,
            path: str,
            endpoint: Endpoint,
            guards: List[EndpointGuard] = None,
    ):
        """
        TODO
        """
        if method == 'GET':
            handler_cls = GetHandler
        elif method == 'POST':
            handler_cls = PostHandler
        else:
            raise RuntimeError('Unsupported HTTP method for endpoints: %s' % method)

        self._flask_app.add_url_rule(
            rule=path,
            endpoint=path,
            methods=[method],
            view_func=handler_cls(
                endpoint=endpoint,
                guards=guards,
            ),
        )

    def run_debug(self, host: str, port: int):
        """
        TODO
        """
        self._flask_app.run(
            host=host,
            port=port,
            debug=True,
        )
