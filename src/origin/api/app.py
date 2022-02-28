import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse 
from fastapi.testclient import TestClient
from functools import cached_property
from typing import List, Iterable, Tuple, Any, Optional

from .guards import EndpointGuard
from .endpoint import Endpoint
from .endpoints import HealthCheck
from .orchestration import \
    RequestOrchestrator, JsonBodyProvider, QueryStringProvider


class Application(object):
    """
    TODO
    """
    def __init__(self, name: str, secret: str):
        self.name = name
        self.secret = secret

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._fastapi_app(*args, **kwargs)

    @classmethod
    def create(
            cls,
            *args,
            endpoints: Iterable[Tuple[str, str, Endpoint]] = (),
            health_check_path: Optional[str] = None,
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
        
        """
        This has to be discussed

        # Add health check endpoint
        if health_check_path:
            app.add_endpoint(
                method='GET',
                path=health_check_path,
                endpoint=HealthCheck(),
            )
        """

        return app

    @cached_property
    def _fastapi_app(self) -> FastAPI:
        """
        TODO
        """
        return FastAPI()

    @property
    def wsgi_app(self) -> FastAPI:
        """
        TODO
        """
        return self._fastapi_app

    @property
    def test_client(self) -> TestClient:
        """
        TODO
        """
        return TestClient(app=self._fastapi_app)

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
            data_provider = QueryStringProvider()
        elif method == 'POST':
            data_provider = JsonBodyProvider()
        else:
            raise RuntimeError(
                f'Unsupported HTTP method for endpoints: {method}'
                )
        
        self._fastapi_app.add_api_route(
            path=path,
            endpoint=endpoint,
            methods=[method],
            response_class=RequestOrchestrator(
                endpoint=endpoint,
                data=data_provider,
                secret=self.secret,
                guards=guards,
            ),
        )

    def run_debug(self, host: str, port: int):
        """
        TODO
        """
        uvicorn.Config.configure_logging(logging.DEBUG)
        uvicorn.run(
            host=host,
            port=port,
            debug=True
        )
