from functools import partial


class HttpResponse(object):
    def __init__(self, status: int, msg: str = ''):
        self.status = status
        self.msg = msg

    @classmethod
    def build(cls, *args, **kwargs):
        return partial(cls, *args, **kwargs)


class HttpError(HttpResponse, Exception):
    def __init__(self, msg: str, status_code: int):
        super(HttpError, self).__init__('%d %s' % (status_code, msg))
        self.msg = msg
        self.status_code = status_code

    @classmethod
    def build(cls, status_code: int, msg: str = ''):
        return partial(cls, status_code=status_code, msg=msg)


BadRequest = HttpError.build(400, 'Bad Request')
Unauthorized = HttpError.build(401, 'Unauthorized')
Forbidden = HttpError.build(403, 'Forbidden')
InternalServerError = HttpError.build(500, 'Internal Server Error')
