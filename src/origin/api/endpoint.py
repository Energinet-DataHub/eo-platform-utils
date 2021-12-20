from abc import abstractmethod
from typing import Optional, Any, Type
from inspect import getfullargspec
from functools import cached_property


class Endpoint(object):
    """
    Represents a single HTTP API endpoint.
    """

    # Request and response schemas (dataclasses or None)
    Request = None
    Response = None

    # view arguments retrieved from the request url path
    # eg. /api/v1/users/<user_id>
    View_args = None

    @abstractmethod
    def handle_request(self, **kwargs) -> Optional[Any]:
        """
        Handle a HTTP request.
        """
        raise NotImplementedError

    @property
    def request_schema(self) -> Optional[Type[Any]]:
        """
        TODO
        """
        return self.Request

    @property
    def response_schema(self) -> Optional[Type[Any]]:
        """
        TODO
        """
        return self.Response

    @property
    def view_args_schema(self) -> Optional[Type[Any]]:
        """
        Variables passed in the URL path. eg. /api/v1/users/<user_id>
        """
        return self.View_args

    @cached_property
    def requires_context(self) -> bool:
        """
        Returns True if handle_request() requires a Context passed as argument.
        """
        return 'context' in getfullargspec(self.handle_request)[0]

    @cached_property
    def should_parse_request_data(self) -> bool:
        """
        Returns True if handle_request() requires an instance of self.Request
        passed as argument.
        """
        return (self.request_schema is not None
                and 'request' in getfullargspec(self.handle_request)[0])

    @cached_property
    def should_parse_view_args(self) -> bool:
        """
        Returns True if handle_request() requires an instance of self.View_args
        passed as argument.
        """
        return (self.view_args_schema is not None
                and 'view_args' in getfullargspec(self.handle_request)[0])
