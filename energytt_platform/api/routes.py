from abc import abstractmethod

from .endpoints import Endpoint


class Route(object):

    @abstractmethod
    def __call__(self, **kwargs):
        pass


class FlaskRoute(Route):
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    def __call__(self, **kwargs):
        self.endpoint.handle_request()
