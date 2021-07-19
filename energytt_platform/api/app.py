from flask import Flask

from .endpoints import Endpoint
from .requests import create_request_handler


class Application(object):
    def __init__(self, name: str):
        self._flask_app = Flask(name)

    @property
    def wsgi_app(self) -> Flask:
        """
        TODO
        """
        return self._flask_app

    def add_endpoint(self, path: str, method: str, endpoint: Endpoint):
        """
        TODO
        """
        self._flask_app.add_url_rule(
            rule=path,
            endpoint=path,
            methods=[method],
            view_func=create_request_handler(
                method=method,
                endpoint=endpoint,
            ),
        )
