import flask
import serpyco
import rapidjson
from abc import abstractmethod
from functools import cached_property
from typing import List, Dict, Any, Optional

from energytt_platform.tokens import TokenEncoder
from energytt_platform.serialize import json_serializer
from energytt_platform.models.auth import InternalToken

from .context import Context
from .flask import FlaskContext
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
        if not flask.request.data:
            return None

        try:
            return rapidjson.loads(flask.request.data.decode('utf8'))
        except rapidjson.JSONDecodeError:
            raise BadRequest('Invalid JSON body provided')


class QueryStringProvider(RequestDataProvider):
    """
    Reads request data from query parameters.
    """
    def get(self) -> Optional[Dict[str, Any]]:
        """
        TODO
        """
        return dict(flask.request.args)


# -- Orchestrator ------------------------------------------------------------


class RequestOrchestrator(object):
    """
    Orchestrates handling of HTTP requests on behalf of an endpoint.

    Behaves as a Flask endpoint, ie. it is callable without taking any
    parameters, so it plugs into Flask seamlessly.
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

    def __call__(self) -> flask.Response:
        """
        Invoked by Flask to handle a HTTP request.
        """
        try:
            return self._invoke_endpoint()
        except HttpResponse as e:
            return self._handle_http_error(e)
        except Exception as e:
            raise
            return self._handle_exception(e)

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
        return FlaskContext(
            token_encoder=self._internal_token_encoder,
        )

    def _invoke_endpoint(self) -> flask.Response:
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
            handler_kwargs['request'] = self._parse_request_data(self.data.get() or {})

        # -- Invoke endpoint -------------------------------------------------

        response = self.endpoint.handle_request(**handler_kwargs)

        # -- Parse response --------------------------------------------------

        status_code = 200
        mimetype = 'text/html'
        headers = {}

        if self.endpoint.should_parse_response_object:
            body = self.endpoint.response_serializer.dump_json(response)
            mimetype = 'application/json'
        elif isinstance(response, HttpResponse):
            status_code = response.status_code
            body = response.body
            headers.update(response.headers)
        elif isinstance(response, (str, bytes)):
            body = response
        elif response is None:
            body = ''
        else:
            # Serialize response object
            raise RuntimeError('INVALID RESPONSE?!')

        return flask.Response(
            status=status_code,
            response=body,
            mimetype=mimetype,
            headers=headers,
        )

    def _handle_http_error(self, e: HttpResponse) -> flask.Response:
        """
        TODO
        """
        return flask.Response(
            status=e.status_code,
            response=e.body_encoded,
            mimetype='text/html',  # TODO
            headers=e.headers,
        )

    def _handle_exception(self, e: Exception) -> flask.Response:
        """
        TODO
        """
        return flask.Response(
            status=500,
            response='Internal Server Error',
            mimetype='text/html',
        )

    def _parse_request_data(self, data: Dict[str, Any]) -> Any:
        """
        TODO
        """
        try:
            return self.endpoint.request_serializer.load(data, True)
        except serpyco.exception.ValidationError as e:
            # JSON schema validation failed for request data
            # TODO Parse ValidationError to something useful
            # TODO Format body properly
            raise BadRequest(body=str(e))

    # def _parse_response_object(self, response: Any) -> str:
    #     """
    #     TODO
    #     """
    #     return self.endpoint.response_serializer.dump_json(response)
