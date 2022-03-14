# Standard Library
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
)
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
        """Debug function for the application."""
        raise NotImplementedError

    def run(self, host: str, port: int):
        """Run function for the application."""
        raise NotImplementedError
