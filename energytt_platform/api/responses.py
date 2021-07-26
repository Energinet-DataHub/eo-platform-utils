from functools import partial


# class HTTPResponse(object):
#     def __init__(self, status: int, msg: str = ''):
#         self.status = status
#         self.msg = msg
#
#     @classmethod
#     def build(cls, *args, **kwargs) -> partial['HTTPResponse']:
#         return partial(cls, *args, **kwargs)


class HttpError(Exception):
    def __init__(self, msg: str, status_code: int):
        super(HttpError, self).__init__('%d %s' % (status_code, msg))
        self.msg = msg
        self.status_code = status_code

    @classmethod
    def build(cls, status_code: int) -> partial['HttpError']:
        return partial(cls, status_code=status_code)


BadRequest = HttpError.build(400, 'Bad Request')
Unauthorized = HttpError.build(401, 'Unauthorized')
InternalServerError = HttpError.build(401, 'Internal Server Error')
