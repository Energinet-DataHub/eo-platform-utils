from typing import List, Dict, Any
from openapi_specgen import (
    OpenApi,
    OpenApiParam,
    OpenApiPath,
    OpenApiResponse,
)

from .app import Application
from .endpoint import Endpoint


class EndpointSpecs(object):
    """
    Generates OpenAPI specs based on an Application object.
    """
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    @property
    def params(self) -> List[OpenApiParam]:
        return []

    @property
    def responses(self) -> List[OpenApiResponse]:
        response = OpenApiResponse(
            descr='Response description',
            data_type=self.endpoint.Response,
        )
        return []


# class OpenApiSpecs(object):
#     """
#     Generates OpenAPI specs based on an Application object.
#     """
#     def __init__(self, app: Application):
#         self.app = app
#
#     @property
#     def specs(self) -> OpenApi:
#         pass


def generate_api_specs(app: Application) -> Dict[str, Any]:
    """
    :param app: Application
    :returns: OpenAPI specs
    """
    paths = []

    for e in app.endpoints:
        specs = EndpointSpecs(e.endpoint)

        path = OpenApiPath(
            path=e.path,
            method=e.method,
            responses=specs.responses,
            params=specs.params,
        )

        paths.append(path)

    return OpenApi(app.title, paths).as_dict()
