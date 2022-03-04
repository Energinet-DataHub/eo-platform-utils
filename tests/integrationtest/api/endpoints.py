from dataclasses import dataclass
from typing import Any

from origin.api import Endpoint, Context
from origin.models.auth import InternalToken


class EmptyEndpoint(Endpoint):
    """Empty endpoints should always return status 200 and empty body."""

    def handle_request(self):
        """TODO."""

        pass


class EndpointReturnsGeneric(Endpoint):
    """Generic endpoint that returns whatever is passed to its constructor."""

    def __init__(self, response: Any):
        """TODO."""

        self.response = response

    def handle_request(self) -> Any:
        """TODO."""

        return self.response


class EndpointRaisesGeneric(Endpoint):
    """Generic endpoint that raises whatever is passed to its constructor."""

    def __init__(self, response: Any):
        """TODO."""

        self.response = response

    def handle_request(self) -> Any:
        """TODO."""

        raise self.response


class EndpointRequiresRequestModel(Endpoint):
    """
    Endpoint that requires an instance of a request model.

    Expected behaviour:
        - The model should be formatted as JSON body
        - "Content-Type" header should be 'application/json'
    """

    @dataclass
    class Request:
        """TODO."""

        something: str

    def handle_request(self, request: Request):
        """TODO."""

        return self.Response(
            success=True,
            something='something',
        )


class EndpointReturnsResponseModel(Endpoint):
    """
    Endpoint that returns body as an instance of a response model.

    Expected behaviour:
        - The model should be formatted as JSON body
        - "Content-Type" header should be 'application/json'
    """

    @dataclass
    class Response:
        """TODO."""

        success: bool
        something: str

    def handle_request(self) -> Response:
        """TODO."""

        return self.Response(
            success=True,
            something='something',
        )


class EndpointWithRequestAndResponseModels(Endpoint):
    """
    Endpoint that takes a request model.
    Returns body as an instance of a response model.

    Expected behaviour:
        - The model should be formatted as JSON body
        - Content-Type header should be 'application/json'
    """

    @dataclass
    class Request:
        """TODO."""

        something: str

    @dataclass
    class Response:
        """TODO."""

        success: bool
        something: str

    def handle_request(self, request: Request) -> Response:
        """TODO."""

        return self.Response(
            success=True,
            something=request.something,
        )


class EndpointRequiresContextReturnsToken(Endpoint):
    """
    Endpoint that returns context.token as JSON (unmodified).

    Expected behaviour:
        - The token is JSON encoded without mutation
    """

    @dataclass
    class Response:
        """TODO."""

        token: InternalToken

    def handle_request(self, context: Context) -> Response:
        """TODO."""

        return self.Response(token=context.token)
