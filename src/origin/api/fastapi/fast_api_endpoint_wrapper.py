# Standard Library
import asyncio
from abc import abstractmethod
from dataclasses import is_dataclass
from functools import partial, wraps
from typing import Any, Dict, List, Optional

# Third party
import flask
import rapidjson
from fastapi.responses import (
    Response as FastApiResponse,
)

# Local
from ..endpoint import Endpoint
from ..guards import EndpointGuard
from ..responses import BadRequest, HttpResponse


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


class RequestDataProvider(object):
    """
    Provides request parameters.
    """
    @abstractmethod
    def get(self) -> Optional[Dict[str, Any]]:
        """
        TODO
        """
        raise NotImplementedError


class JsonBodyProvider(RequestDataProvider):
    """
    Reads request data from request body JSON.
    """

    def get(self) -> Optional[Dict[str, Any]]:
        """
        TODO
        """
        if not flask.request.data:
            return None

        try:
            return rapidjson.loads(flask.request.data.decode('utf8'))
        except rapidjson.JSONDecodeError:
            raise BadRequest('Invalid JSON body provided')


class FastAPIEndpointWrapper(object):

    def __init__(
        self,
        endpoint: Endpoint,
        methods: List[str],
        # data: RequestDataProvider,
        secret: str,
        guards: List[EndpointGuard] = None,
    ):
        self.endpoint = endpoint
        # self.data = data
        self.secret = secret
        self.guards = guards

    def construct_response(self, return_value) -> HttpResponse:
        if isinstance(return_value, HttpResponse):
            response = return_value
        elif is_dataclass(return_value):
            response = HttpResponse(status=200, model=return_value)
        elif isinstance(return_value, (str, bytes)):
            response = HttpResponse(status=200, body=return_value)
        elif isinstance(return_value, dict):
            response = HttpResponse(status=200, json=return_value)
        elif return_value is None:
            response = HttpResponse(status=200)
        else:
            # TODO Handle this
            raise RuntimeError('ENDPOINT RETURNED INVALID RESPONSE?!?!?')

        fastapi_response = FastApiResponse(
            status_code=response.status,
            content=response.actual_body,
            headers=response.actual_headers,
            media_type=response.actual_mimetype,
        )

        for cookie in response.cookies:
            fastapi_response.set_cookie(
                key=cookie.name,
                value=cookie.value,
                expires=cookie.expires,
                path=cookie.path,
                domain=cookie.domain,
                secure=cookie.secure,
                httponly=cookie.http_only,
                samesite='Strict' if cookie.same_site else 'None',
            )

        return fastapi_response

    def handle_request(self, *args, **kwargs):
        try:
            return self._invoke_endpoint(*args, **kwargs)
        except HttpResponse as e:
            return self._handle_http_error(e)
        except Exception as e:
            return self._handle_exception(e)

    def get_wrapped_endpoint(self):
        @wraps(self.endpoint.handle_request)
        def wrapped_func(*args, **kwargs):
            return self.handle_request(*args, **kwargs)

        return wrapped_func

    def _invoke_endpoint(self, *args, **kwargs):

        return_value = self.endpoint.handle_request(*args, **kwargs)

        response = self.construct_response(return_value)
        return response

    def _handle_http_error(self, e: HttpResponse) -> flask.Response:
        """
        TODO
        """
        return FastApiResponse(
            status_code=e.status,
            content=e.body,
            headers=e.headers,
            media_type='text/html',
        )

    def _handle_exception(self, e: Exception) -> flask.Response:
        """
        TODO
        """
        return FastApiResponse(
            status_code=500,
            content='Internal Server Error',
            media_type='text/html',
        )
