import rapidjson
from datetime import datetime
from functools import partial, cached_property
from http.cookies import SimpleCookie
from typing import List, Dict, Any, Optional, Union, TypeVar, Generic, Tuple
from dataclasses import dataclass, field, is_dataclass

from energytt_platform.serialize import json_serializer

from .cookies import Cookie


TResponseModel = TypeVar('TResponseModel')


@dataclass
class HttpResponse(Generic[TResponseModel], Exception):
    """
    TODO
    """

    # HTTP Status Code
    status: int

    # Response body
    body: Optional[Union[str, bytes]] = \
        field(default=None)

    # Response body JSON
    json: Optional[Dict[str, Any]] = \
        field(default=None)

    # Response model
    model: Optional[TResponseModel] = \
        field(default=None)

    # Response headers
    headers: Dict[str, str] = \
        field(default_factory=dict)

    # Response cookies
    cookies: Union[List[Cookie], Tuple[Cookie, ...]] = \
        field(default_factory=tuple)

    # def __init__(
    #         self,
    #         status: int,
    #         body: Optional[Any] = None,
    #         headers: Dict[str, str] = None,
    #         cookies: List[Cookie] = None,
    # ):
    #     """
    #     TODO
    #
    #     :param status:
    #     :param body:
    #     :param headers:
    #     :param cookies:
    #     """
    #     self.status = status
    #     self.body = body
    #     self.headers = headers or {}
    #     self.cookies = cookies or []

    @cached_property
    def actual_headers(self) -> Dict[str, str]:
        """
        TODO
        """
        headers = {}
        headers.update(self.headers)

        # if self.cookies:
        #     headers['Set-Cookie'] = self.get_cookies_header()

        return headers

    # def get_cookies_header(self) -> str:
    #     """
    #     TODO
    #     """
    #     cookies = SimpleCookie()
    #
    #     for c in self.cookies:
    #         cookies[c.name] = c.value
    #         if c.path:
    #             cookies[c.name]['path'] = c.path
    #
    #     return cookies.output(header='').strip()

    @cached_property
    def actual_body(self) -> Optional[Union[str, bytes]]:
        """
        TODO
        """
        if self.body is not None:
            return self.body
        elif self.json is not None:
            return rapidjson.dumps(self.json)
        elif self.model is not None:
            return json_serializer.serialize(self.model)
        else:
            return None

    @cached_property
    def actual_mimetype(self) -> Optional[Union[str, bytes]]:
        """
        TODO
        """
        if self.body is not None:
            return 'text/html'
        elif self.json is not None:
            return 'application/json'
        elif self.model is not None:
            return 'application/json'
        else:
            return 'text/html'

        # if isinstance(self.body, dict) or is_dataclass(self.body):
        # else:


class HttpError(HttpResponse):
    """
    TODO
    """
    def __init__(self, msg: str, status: int, **kwargs):
        kwargs.setdefault('body', f'{status} {msg}')
        super(HttpError, self).__init__(status=status, **kwargs)


# def create_http_response()


# class HttpError(HttpResponse, Exception):
#     def __init__(self, status_code: int, msg: str, body: str = None):
#         Exception.__init__(self, msg)
#         HttpResponse.__init__(self, status_code, body)


# TemporaryRedirect = HttpError.build(307, 'Temporary Redirect')
# BadRequest = HttpResponse.build(400, 'Bad Request')
# Unauthorized = HttpResponse.build(401, 'Unauthorized')
# Forbidden = HttpResponse.build(403, 'Forbidden')
# InternalServerError = HttpResponse.build(500, 'Internal Server Error')


class MovedPermanently(HttpResponse):
    def __init__(self, url, **kwargs):
        super(MovedPermanently, self).__init__(
            status=301, headers={'Location': url}, **kwargs)


class TemporaryRedirect(HttpResponse):
    def __init__(self, url, **kwargs):
        super(TemporaryRedirect, self).__init__(
            status=307, headers={'Location': url}, **kwargs)


class BadRequest(HttpError):
    def __init__(self, **kwargs):
        super(BadRequest, self).__init__(
            status=400, msg='Bad Request', **kwargs)


class Unauthorized(HttpError):
    def __init__(self, msg: str = 'Unauthorized', **kwargs):
        super(Unauthorized, self).__init__(
            status=401, msg=msg, **kwargs)


class Forbidden(HttpError):
    def __init__(self, msg: str = 'Forbidden', **kwargs):
        super(Forbidden, self).__init__(
            status=403, msg=msg, **kwargs)


class InternalServerError(HttpError):
    def __init__(self, msg: str = 'Internal Server Error', **kwargs):
        super(InternalServerError, self).__init__(
            status=500, msg=msg, **kwargs)
