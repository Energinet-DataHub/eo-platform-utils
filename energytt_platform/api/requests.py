import serpyco
import rapidjson
from abc import abstractmethod
from functools import cached_property
from typing import Dict, Optional, Any

from flask import Response, request
from werkzeug.exceptions import HTTPException, BadRequest

from .endpoints import Endpoint


class RequestHandler(object):
    """
    Abstract base class for http controllers, written specifically for Flask.
    """
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    # -- Request and Response (de)serialization ------------------------------

    @cached_property
    def request_serializer(self) -> Optional[serpyco.Serializer]:
        """
        TODO
        """
        return self.build_request_serializer() \
            if self.endpoint.Request is not None \
            else None

    @cached_property
    def response_serializer(self) -> Optional[serpyco.Serializer]:
        """
        TODO
        """
        return self.build_response_serializer() \
            if self.endpoint.Response is not None \
            else None

    def build_request_serializer(self) -> serpyco.Serializer:
        """
        :rtype: Serializer
        """
        encoders = {}
        # encoders.update(default_encoders)
        encoders.update(self.get_encoders())
        return serpyco.Serializer(self.endpoint.Request, type_encoders=encoders)

    def build_response_serializer(self) -> serpyco.Serializer:
        """
        :rtype: Serializer
        """
        encoders = {}
        # encoders.update(default_encoders)
        encoders.update(self.get_encoders())
        return serpyco.Serializer(self.endpoint.Response, type_encoders=encoders)

    def get_encoders(self) -> Dict[Any, serpyco.FieldEncoder]:
        """
        TODO
        """
        return {}

    # -- HTTP request handling -----------------------------------------------

    # @abstractmethod
    # def handle_request(self, **kwargs):
    #     """
    #     Handle the HTTP request. Overwritten by subclassing.
    #     """
    #     raise NotImplementedError

    def __call__(self):
        """
        Invoked by Flask to handle a HTTP request.
        """
        try:
            return self.invoke_endpoint()
        except HTTPException as e:
            return self.handle_exception(e)
        except Exception as e:
            return self.handle_exception(e)

    def invoke_endpoint(self):
        """
        :rtype: flask.Response
        """
        kwargs = {}

        if self.request_serializer is not None:
            kwargs['request'] = self.get_request_vm()

        handler_response = self.endpoint.handle_request(**kwargs)
        response = self.parse_response(handler_response)

        if isinstance(response, str):
            return Response(
                status=200,
                mimetype='application/json',
                response=response,
            )
        else:
            return response

    def handle_exception(self, e):
        """
        :param Exception e:
        :rtype: Response
        """
        # if DEBUG and not isinstance(e, HTTPException):
        #     raise e

        body = {'success': False}

        if hasattr(e, 'description'):
            if isinstance(e.description, str):
                body['message'] = e.description
            elif isinstance(e.description, dict):
                body['errors'] = e.description

        return Response(
            status=e.code if hasattr(e, 'code') else 500,
            mimetype='application/json',
            response=rapidjson.dumps(body),
        )

    @abstractmethod
    def get_request_vm(self):
        """
        Converts JSON provided in the request body according to the Schema
        defined on self.Request (if any), and returns the model instance.
        Returns None if self.Requests is None.

        :rtype: typing.Any
        """
        raise NotImplementedError
        # try:
        #     return serializer.load_(params)
        # except ValidationError as e:
        #     raise BadRequest(e.messages)

    def parse_response(self, response):
        """
        Converts the return value of handle_request() into a HTTP response
        body.
        :param obj response: The object returned by handle_request()
        :rtype: str
        :returns: HTTP response body
        """
        if response is None:
            return ''
        elif response in (True, False):
            return rapidjson.dumps({'success': response})
        elif isinstance(response, dict):
            return rapidjson.dumps(response)
        elif isinstance(response, (Response, wResponse)):
            return response
        elif self.response_serializer is not None:
            return self.response_serializer.dump_json(response)
        else:
            raise RuntimeError('Unknown response: %s' % str(response))


class PostHandler(RequestHandler):
    """
    Handles HTTP POST requests.
    """
    methods = ['POST']

    def get_request_vm(self):
        """
        :rtype: typing.Any
        """
        # TODO Check Content-Type header

        if not request.data:
            raise BadRequest('No JSON body provided')

        # try:
        #     params.update(json.loads(request.data))
        # except json.JSONDecodeError:
        #     raise BadRequest('Bad JSON body provided')

        try:
            return self.request_serializer.load_json(
                request.data.decode('utf8'), True)
        except rapidjson.JSONDecodeError as e:
            raise BadRequest('Invalid JSON body provided')
        except serpyco.exception.ValidationError as e:
            raise BadRequest(str(e))


        # return super(PostHandler, self) \
        #     .get_request_vm(schema, **params)


class GetHandler(RequestHandler):
    """
    Handles HTTP GET requests.
    """
    methods = ['GET']

    def get_request_vm(self):
        """
        :rtype: typing.Any
        """
        return self.request_serializer.load(dict(request.args), True)


def create_request_handler(method: str, *args, **kwargs) -> RequestHandler:
    pass
