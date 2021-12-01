import logging
from dataclasses import dataclass, field

from flask import Flask
from flask.testing import FlaskClient
from functools import cached_property
from typing import List, Iterable, Tuple, Any, Optional

from .guards import EndpointGuard
from .endpoint import Endpoint
from .endpoints import HealthCheck, OpenApiSwaggerUI, OpenApiSpecs
from .orchestration import \
    RequestOrchestrator, JsonBodyProvider, QueryStringProvider


@dataclass
class EndpointDescription:
    method: str
    path: str
    endpoint: Endpoint
    guards: List[EndpointGuard] = field(default_factory=list)


class Application(object):
    """
    TODO
    """
    def __init__(
            self,
            title: str,
            base_url: str,
            secret: str,
            description: Optional[str] = None,
    ):
        """
        :param title: Application title
        :param base_url: Application absolute URL, without trailing slash
        :param secret: Application secret
        :param description: Application description
        """
        self.title = title
        self.base_url = base_url
        self.secret = secret
        self.description = description
        self.endpoints: List[EndpointDescription] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._flask_app(*args, **kwargs)

    @classmethod
    def create(
            cls,
            *args,
            endpoints: Iterable[Tuple[str, str, Endpoint]] = (),
            health_check_path: Optional[str] = None,
            docs_path: Optional[str] = None,
            **kwargs,
    ) -> 'Application':
        """
        Create a new instance of an Application
        """

        app = cls(*args, **kwargs)

        # Add endpoints
        for e in endpoints:
            assert 3 <= len(e) <= 4

            method, path, endpoint = e[:3]

            if len(e) == 4:
                guards = e[3]
            else:
                guards = []

            app.add_endpoint(
                method=method,
                path=path,
                endpoint=endpoint,
                guards=guards,
            )

        if health_check_path:
            app.add_health_check_endpoint(health_check_path)
        if docs_path:
            app.add_docs_endpoints(docs_path)

        return app

    @cached_property
    def _flask_app(self) -> Flask:
        """
        TODO
        """
        return Flask(self.title)

    @property
    def wsgi_app(self) -> Flask:
        """
        TODO
        """
        return self._flask_app

    @property
    def test_client(self) -> FlaskClient:
        """
        TODO
        """
        return self._flask_app.test_client()

    # @property
    # def endpoints(self) -> Iterable[Tuple[str, Endpoint]]:
    #     """
    #     TODO
    #     """
    #     yield from self._flask_app.view_functions.items()
    #
    #     return self._flask_app.test_client()

    def add_endpoint(
            self,
            method: str,
            path: str,
            endpoint: Endpoint,
            guards: List[EndpointGuard] = None,
    ):
        """
        Adds a new endpoint to the app.

        :param method: HTTP method (upper-case)
        :param path: Path relative to root without trailing slash
        :param endpoint: The endpoint object
        :param guards: Optional guards
        """
        if method == 'GET':
            data_provider = QueryStringProvider()
        elif method == 'POST':
            data_provider = JsonBodyProvider()
        else:
            raise RuntimeError(
                'Unsupported HTTP method for endpoints: %s' % method)

        self.endpoints.append(EndpointDescription(
            method=method,
            path=path,
            endpoint=endpoint,
            guards=guards,
        ))

        self._flask_app.add_url_rule(
            rule=path,
            endpoint=path,
            methods=[method],
            view_func=RequestOrchestrator(
                endpoint=endpoint,
                data=data_provider,
                secret=self.secret,
                guards=guards,
            ),
        )

    def add_health_check_endpoint(self, health_check_path: str):
        """
        Adds a health check endpoint to the app.

        :param health_check_path: Base path without trailing slash
        """
        self.add_endpoint(
            method='GET',
            path=health_check_path,
            endpoint=HealthCheck(),
        )

    def add_docs_endpoints(self, docs_path: str):
        """
        Adds docs endpoints to the app.

        :param docs_path: Base path without trailing slash
        """
        specs_path = f'{docs_path}/openapi'
        specs_url = f'{self.base_url}{specs_path}'

        self.add_endpoint(
            method='GET',
            path=docs_path,
            endpoint=OpenApiSwaggerUI(
                specs_url=specs_url,
            ),
        )

        self.add_endpoint(
            method='GET',
            path=specs_path,
            endpoint=OpenApiSpecs(
                app=self,
            ),
        )

    def run_debug(self, host: str, port: int):
        """
        Runs a debug server for local development only.

        :param host: Hostname to listen on
        :param port: Port to listen on
        """
        self._flask_app.logger.setLevel(logging.DEBUG)
        self._flask_app.run(
            host=host,
            port=port,
            debug=True,
        )
