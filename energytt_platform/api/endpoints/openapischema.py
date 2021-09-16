from ..app import Application
from ..endpoint import Endpoint


class OpenApiSchema(Endpoint):
    """
    TODO
    """
    def __init__(self, app: Application):
        self.app = app

    def handle_request(self):
        pass
