# Standard Library
import asyncio
import logging
from functools import (
    cached_property,
    partial,
    wraps,
)
import secrets
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
)

from click import secho

from .fast_api_endpoint_wrapper import FastAPIEndpointWrapper
# Third party
from fastapi import FastAPI
from fastapi.testclient import TestClient

from flask import Flask
from flask.testing import FlaskClient

# Local
from .endpoint import Endpoint
from .endpoints import HealthCheck
from .guards import EndpointGuard
from .orchestration import (
    JsonBodyProvider,
    QueryStringProvider,
    RequestOrchestrator,
)


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


class Application(object):
    """
    Create a new instance of the application and adds all the endpoints to it.

    :return: The Application instance.
    """

    def __init__(self, name: str, secret: str):
        self.name = name
        self.secret = secret

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """TODO."""
        return self._flask_app(*args, **kwargs)

    @classmethod
    def create(
            cls,
            *args,
            endpoints: Iterable[Tuple[str, str, Endpoint]] = (),
            health_check_path: Optional[str] = None,
            **kwargs,
    ) -> 'Application':
        """Create a new instance of an Application."""

        app = cls(*args, **kwargs)

        # Add endpoints
        # for e in endpoints:
        #     assert 3 <= len(e) <= 4

        #     method, path, endpoint = e[:3]

        #     if len(e) == 4:
        #         guards = e[3]
        #     else:
        #         guards = []

        #     app.add_endpoint(
        #         method=method,
        #         path=path,
        #         endpoint=endpoint,
        #         guards=guards,
        #     )

        # Add health check endpoint
        if health_check_path:
            app.add_endpoint(
                method='GET',
                path=health_check_path,
                endpoint=HealthCheck(),
            )

        return app

    @cached_property
    def _fast_api_app(self) -> FastAPI:
        """FastAPI application instance."""
        return FastAPI()

    @property
    def wsgi_app(self) -> FastAPI:
        """Web Server Gateway Interface application instance."""
        return self._fast_api_app

    @property
    def test_client(self) -> FlaskClient:
        """Test client application instance."""
        return TestClient(self._fast_api_app)


    def add_endpoint(
            self,
            method: str,
            path: str,
            endpoint: Endpoint,
            guards: List[EndpointGuard] = None,
    ):
        """Add endpoints to the application."""

        if method == 'GET':
            data_provider = QueryStringProvider()
        elif method == 'POST':
            data_provider = JsonBodyProvider()
        else:
            raise RuntimeError(
                'Unsupported HTTP method for endpoints: %s' % method)

        endpoint_wrapper = FastAPIEndpointWrapper(
            endpoint=endpoint,
            secret="",
            methods=[method],

        )

        wrapped_endpoint = endpoint_wrapper.get_wrapped_endpoint()

        # wrapped_endpoint = async_wrap(endpoint)

        self._fast_api_app.add_api_route(
            path=path,
            methods=[method],
            endpoint=wrapped_endpoint,
            response_model=endpoint.Response,
        )

        # self._fast_api_app.add_url_rule(
        #     rule=path,
        #     endpoint=path,
        #     methods=[method],
        #     view_func=RequestOrchestrator(
        #         endpoint=endpoint,
        #         data=data_provider,
        #         secret=self.secret,
        #         guards=guards,
        #     ),
        # )

    def run_debug(self, host: str, port: int):
        """Debug function for the Flask application."""
        # self._fast_api_app.logger.setLevel(logging.DEBUG)
