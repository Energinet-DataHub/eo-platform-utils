from functools import partial
from typing import Dict, Any, Optional


class HttpResponse(Exception):
    def __init__(
            self,
            status_code: int,
            body: str = None,
            headers: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.body = body
        self.headers = headers

    @classmethod
    def build(cls, *args, **kwargs):
        return partial(cls, *args, **kwargs)

    @property
    def body_encoded(self) -> str:
        # TODO Encode dataclasses etc..
        return str(self.body) if self.body else ''


class HttpError(HttpResponse):
    """
    TODO
    """
    def __init__(self, msg: str, status_code: int, **kwargs):
        kwargs.setdefault('body', f'{status_code} {msg}')
        super(HttpError, self).__init__(status_code=status_code, **kwargs)


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
            status_code=301,
            headers={'Location': url},
            **kwargs,
        )


class TemporaryRedirect(HttpResponse):
    def __init__(self, url, **kwargs):
        super(TemporaryRedirect, self).__init__(
            status_code=307,
            headers={'Location': url},
            **kwargs,
        )


class BadRequest(HttpError):
    def __init__(self, **kwargs):
        super(BadRequest, self).__init__(
            status_code=400,
            msg='Bad Request',
            **kwargs,
        )


class Unauthorized(HttpError):
    def __init__(self, msg: str = 'Unauthorized', **kwargs):
        super(Unauthorized, self).__init__(
            status_code=401,
            msg=msg,
            **kwargs,
        )


class Forbidden(HttpError):
    def __init__(self, msg: str = 'Forbidden', **kwargs):
        super(Forbidden, self).__init__(
            status_code=403, msg=msg, **kwargs)


class InternalServerError(HttpError):
    def __init__(self, msg: str = 'Internal Server Error', **kwargs):
        super(InternalServerError, self).__init__(
            status_code=500, msg=msg, **kwargs)
