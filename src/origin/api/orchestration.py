"""Modules."""
from dataclasses import is_dataclass
from abc import abstractmethod
from functools import cached_property
from typing import List, Dict, Any, Optional, Type

import fastapi
import serpyco
import rapidjson

from src.origin.tokens import TokenEncoder
from src.origin.serialize import simple_serializer
from src.origin.models.auth import InternalToken

from .context import Context
from .fastapi import FastapiContext
from .endpoint import Endpoint
from .guards import EndpointGuard, bouncer
from .responses import HttpResponse, BadRequest


# -- Request data ------------------------------------------------------------


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
        if not fastapi.requests.Request.body:
            return None

        try:
            return rapidjson.loads(fastapi.requests.Request.body.decode("utf8"))
        except rapidjson.JSONDecodeError:
            raise BadRequest('Invalid JSON body provided') from rapidjson.JSONDecodeError


class QueryStringProvider(RequestDataProvider):
    """
    Reads request data from query parameters.
    """
    def get(self) -> Optional[Dict[str, Any]]:
        """
        TODO
        """
        return dict(fastapi.requests.Request.body.args)


# -- Orchestrator ------------------------------------------------------------


class RequestOrchestrator(object):
    """
    Orchestrates handling of HTTP requests on behalf of an endpoint.

    Behaves as a fastapi endpoint, ie. it is callable without taking any
    parameters, so it plugs into fastapi seamlessly.
    """
    def __init__(
            self,
            endpoint: Endpoint,
            data: RequestDataProvider,
            secret: str,
            guards: List[EndpointGuard] = None,
    ):
        self.endpoint = endpoint
        self.data = data
        self.secret = secret
        self.guards = guards

    def __call__(self) -> fastapi.requests.Request.body:
        """
        Invoked by fastapi to handle a HTTP request.
        """
        try:
            return self._invoke_endpoint()
        except HttpResponse as err:
            return self._handle_http_error(err)
        except Exception as err:
            raise Exception from err

    @cached_property
    def _internal_token_encoder(self) -> TokenEncoder[InternalToken]:
        """
        TODO
        """
        return TokenEncoder(
            schema=InternalToken,
            secret=self.secret,
        )

    def _build_context(self) -> Context:
        """
        Creates a new request context.
        """
        return FastapiContext(
            token_encoder=self._internal_token_encoder,
        )

    def _invoke_endpoint(self) -> fastapi.requests.Request.body:
        """
        TODO
        """
        context = self._build_context()

        if self.guards:
            bouncer.validate(context, self.guards)

        # -- Define arguments for handler ------------------------------------

        handler_kwargs = {}

        if self.endpoint.requires_context:
            handler_kwargs['context'] = context

        # Deserialize request data (if necessary)
        if self.endpoint.should_parse_request_data:
            # Defaulting to an empty dictionary makes it possible to omit
            # request data for models where all fields are optional
            handler_kwargs['request'] = self._parse_request_data(
                data=self.data.get() or {},
                schema=self.endpoint.request_schema,
            )

        # -- Invoke endpoint -------------------------------------------------

        return_value = self.endpoint.handle_request(**handler_kwargs)

        # -- Parse return value ----------------------------------------------

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

        # -- Create fastapi response -------------------------------------------

        fastapi_response = fastapi.responses.JSONResponse(
            status=response.status,
            mimetype=response.actual_mimetype,
            headers=response.actual_headers,
            response=response.actual_body,
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

    def _handle_http_error(self, e: HttpResponse) -> fastapi.responses.JSONResponse:
        """
        TODO
        """
        return fastapi.responses.JSONResponse(
            status=e.status,
            response=e.body,
            mimetype='text/html',  
            headers=e.headers,
        )

    def _handle_exception(self, err: Exception) -> fastapi.responses.JSONResponse:
        """
        TODO
        """
        return fastapi.responses.JSONResponse(
            status=500,
            response='Internal Server Error',
            mimetype='text/html',
        )

    def _parse_request_data(
            self,
            data: Dict[str, Any],
            schema: Type[Any],
    ) -> Any:
        """
        TODO
        """
        try:
            return simple_serializer.deserialize(
                data=data,
                schema=schema,
            )
        except serpyco.exception.ValidationError as err:
            # JSON schema validation failed for request data
            # TODO Parse ValidationError to something useful
            # TODO Format body properly
            raise BadRequest(body=str(err)) from serpyco.exception.ValidationError

    # def _parse_response_object(self, response: Any) -> str:
    #     """
    #     TODO
    #     """
    #     return self.endpoint.response_serializer.dump_json(response)
