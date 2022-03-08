# Standard Library
from functools import cached_property
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
)

# Third party
from fastapi import FastAPI
from flask.testing import FlaskClient

# Local
from .endpoint import Endpoint
from .guards import EndpointGuard


class Application(object):
    """
    Base application, used to create a instance which contains endpoints.

    :return: The Application instance.
    """

    def __init__(self, name: str, secret: str):
        self.name = name
        self.secret = secret

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """TODO."""
        raise NotImplementedError

    @classmethod
    def create(
            cls,
            *args,
            endpoints: Iterable[Tuple[str, str, Endpoint]] = (),
            health_check_path: Optional[str] = None,
            **kwargs,
    ) -> 'Application':
        """Create a new instance of an Application."""
        raise NotImplementedError

    @cached_property
    def _fast_api_app(self) -> FastAPI:
        """FastAPI application instance."""
        raise NotImplementedError

    @property
    def wsgi_app(self) -> FastAPI:
        """Web Server Gateway Interface application instance."""
        raise NotImplementedError

    @property
    def test_client(self) -> FlaskClient:
        """Test client application instance."""
        raise NotImplementedError

    def add_endpoint(
            self,
            method: str,
            path: str,
            endpoint: Endpoint,
            guards: List[EndpointGuard] = None,
    ):
        """Add endpoints to the application."""
        raise NotImplementedError

    def run_debug(self, host: str, port: int):
        """Debug function for the Flask application."""
        raise NotImplementedError
