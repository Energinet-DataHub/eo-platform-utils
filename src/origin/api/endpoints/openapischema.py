from ..endpoint import Endpoint


class OpenApiSchema(Endpoint):
    """OpenAPI Schema endpoint."""

    def __init__(self, app):
        self.app = app

    def handle_request(self):
        """Handle request."""

        pass
