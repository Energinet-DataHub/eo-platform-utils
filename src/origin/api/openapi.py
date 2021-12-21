"""
OpenAPI specifications:
https://swagger.io/specification/
"""
from enum import Enum
from functools import cached_property

from serpyco import field
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Union

from apispec import APISpec
from dataclasses_jsonschema.apispec import DataclassesPlugin
from dataclasses_jsonschema import JsonSchemaMixin, SchemaType

from .endpoint import Endpoint


def generate_api_specs(app: 'Application') -> Dict[str, Any]:
    spec = APISpec(
        title=app.title,
        version='1.0.0',
        openapi_version='3.0.2',
        plugins=[DataclassesPlugin()],
    )

    spec.path(
        path='/test',
        summary='This is Path Summary!',
        description='This is Path Description!',
        # operations={
        #     'summary': 'This is the PathItem summary!',
        #     'description': 'This is the PathItem description!',
        #     'get': {
        #         'tags': [{'name': 'tag1'}, {'name': 'tag2'}],
        #         'summary': 'This is the Operation summary!',
        #         'description': 'This is the Operation description!',
        #         'operationId': 'This is the Operation operationId!',
        #         'requestBody': {
        #             'application/json': {}
        #         }
        #     }
        # }
    )

    spec.components.schema(
        component_id='MyModel',
        schema=MyModel,
    )

    return spec.to_dict()

#
#
# @dataclass
# class Contact:
#     pass
#
#
# @dataclass
# class License:
#     pass
#
#
# @dataclass
# class ExternalDocumentation:
#     pass
#
#
# @dataclass
# class Tag:
#     name: str
#     description: Optional[str] = field(default=None)
#     externalDocs: Optional[ExternalDocumentation] = field(default=None)
#
#
# @dataclass
# class Info:
#     title: str
#     version: str
#     # description: Optional[str] = field(default=None)
#     # termsOfService: Optional[str] = field(default=None)
#     # contact: Optional[Contact] = field(default=None)
#     # license: Optional[License] = field(default=None)
#
#
# @dataclass
# class Server:
#     pass
#
#
# class ParameterIn(Enum):
#     query = 'query'
#     header = 'header'
#     path = 'path'
#     cookie = 'cookie'
#
#
# @dataclass
# class Parameter:
#     name: str
#     in_: Optional[ParameterIn] = field(default=None, dict_key='in')
#     description: Optional[str] = field(default=None)
#     required: Optional[bool] = field(default=None)
#     deprecated: Optional[bool] = field(default=None)
#     allowEmptyValue: Optional[bool] = field(default=None)
#
#
# @dataclass
# class Reference:
#     pass
#
#
# @dataclass
# class MediaType:
#     pass
#
#
# @dataclass
# class RequestBody:
#     description: Optional[str] = field(default=None)
#     required: Optional[bool] = field(default=None)
#     content: Dict[str, MediaType] = field(default_factory=dict)
#
#
# @dataclass
# class Response:
#     pass
#
#
# @dataclass
# class Operation:
#     tags: List[Tag] = field(default_factory=list)
#     summary: Optional[str] = field(default=None)
#     description: Optional[str] = field(default=None)
#     externalDocs: Optional[ExternalDocumentation] = field(default=None)
#     operationId: Optional[str] = field(default=None)
#     parameters: List[Union[Parameter, Reference]] \
#         = field(default_factory=list)
#     requestBody: Optional[Union[RequestBody, Reference]]\
#         = field(default=None)
#     responses: Dict[str, Union[Response, Reference]] \
#         = field(default_factory=dict)
#
#
# @dataclass
# class PathItem:
#     ref: Optional[str] = field(default=None, dict_key='$ref')
#     summary: Optional[str] = field(default=None)
#     description: Optional[str] = field(default=None)
#     get: Optional[Operation] = field(default=None)
#     # put: Optional[Operation] = field(default=None)
#     # post: Optional[Operation] = field(default=None)
#     # delete: Optional[Operation] = field(default=None)
#     # options: Optional[Operation] = field(default=None)
#     # head: Optional[Operation] = field(default=None)
#     # patch: Optional[Operation] = field(default=None)
#     # trace: Optional[Operation] = field(default=None)
#     servers: List[Server] = field(default_factory=list)
#     parameters: List[Union[Parameter, Reference]] \
#         = field(default_factory=list)
#
#
# @dataclass
# class Schema:
#     pass
#
#
# @dataclass
# class Components:
#     schemas: Dict[str, Union[Schema, Reference]] \
#         = field(default_factory=dict)
#
#     responses: Dict[str, Union[Response, Reference]] \
#         = field(default_factory=dict)
# #
# #
# # @dataclass
# # class SecurityRequirement:
# #     pass
#
#
# @dataclass
# class OpenApi:
#     info: Info
#     openapi: str = field(default='3.0.3')
#     # servers: List[Server] = field(default_factory=list)
#     paths: Dict[str, PathItem] = field(default_factory=dict)
#     components: Optional[Components] = field(default=None)
#     # security: Optional[SecurityRequirement] = field(default=None)
#     # tags: List[Tag] = field(default_factory=list)
#     # externalDocs: Optional[ExternalDocumentation] = field(default=None)
#
#     def add_path(self, path: str, path_item: PathItem):
#         """
#         :param path: Path relative from root, prefixed with a slash
#         :param path_item: The PathItem to add
#         """
#         assert path[0] == '/', 'Path must be prefixed with a slash (/)'
#         assert path not in self.paths, 'Path already defined'
#
#         self.paths[path] = path_item
#
#     def as_dict(self, include_empty: bool = False) -> Dict[str, Any]:
#         """
#         :param include_empty: Whether to include None or empty values
#         :returns: OpenAPI specs as a dictionary, ready for JSON serialization
#         """
#         return asdict(self)
#
#
# ##############################################################################
# ##############################################################################
# ##############################################################################
#
#
# # class OpenApiGenerator(object):
# #     def __init__(self):
# #         self.components = []
#
#
# def generate_request_body(endpoint: Endpoint) -> Dict[str, Any]:
#
#     class Request(endpoint.request_schema, JsonSchemaMixin):
#         pass
#
#     schema = Request.json_schema(schema_type=SchemaType.DRAFT_04)
#
#     return {
#         'description': 'Request body description',
#         'required': True,
#         'content': {
#             'application/json': {
#                 'schema': schema,
#             }
#         }
#     }
#
#
# def generate_parameters(endpoint: Endpoint) -> List[Dict[str, Any]]:
#
#     class Request(endpoint.request_schema, JsonSchemaMixin):
#         pass
#
#     params = []
#     schema = Request.json_schema()
#
#     for name, prop in schema['properties'].items():
#         params.append({
#             'in': 'query',
#             'name': name,
#             'required': name in schema.get('required', ()),
#             'schema': schema['properties'][name],
#         })
#
#     return params
#
#
# def generate_endpoint_specs(
#         path: str,
#         method: str,
#         endpoint: Endpoint,
# ) -> Dict[str, Any]:
#
#     path_item = {
#         # 'tags': [{'name': 'tag1'}, {'name': 'tag2'}],
#         'summary': 'This is the Operation summary!',
#         'description': endpoint.__doc__,
#         'operationId': path,
#     }
#
#     if endpoint.request_schema:
#         if method == 'GET':
#             path_item['parameters'] = generate_parameters(endpoint)
#         elif endpoint.request_schema and method in ('POST', 'PUT'):
#             path_item['requestBody'] = generate_request_body(endpoint)
#         else:
#             raise RuntimeError('Unsupported METHOD')
#
#     return {
#         'summary': endpoint.__doc__,
#         'description': endpoint.__doc__,
#         method.lower(): path_item,
#         # 'parameters': [
#         #     {
#         #         'in': 'query',
#         #         'name': 'param1',
#         #         'required': True,
#         #         'schema': {}
#         #     }
#         # ]
#     }
#
#
# def generate_api_specs(app: 'Application') -> Dict[str, Any]:
#
#     paths = {}
#
#     for e in app.endpoints:
#         paths[e.path] = generate_endpoint_specs(
#             path=e.path,
#             endpoint=e.endpoint,
#             method=e.method,
#         )
#
#     return {
#         'openapi': '3.0.3',
#         'info': {
#             'title': app.title,
#             'version': '1.0.0',
#         },
#         'paths': paths,
#         # 'paths': {
#         #     '/test-path': {
#         #         'summary': 'This is Path Summary!',
#         #         'description': 'This is Path Description!',
#         #         'post': {
#         #             'tags': [{'name': 'tag1'}, {'name': 'tag2'}],
#         #             'summary': 'This is the Operation summary!',
#         #             'description': 'This is the Operation description!',
#         #             'operationId': 'This is the Operation operationId!',
#         #             'requestBody': {
#         #                 'description': 'Request body description',
#         #                 'required': True,
#         #                 'content': {
#         #                     'application/json': {
#         #                         'schema': MyModel.json_schema(),
#         #                     }
#         #                 }
#         #             }
#         #         }
#         #     }
#         # },
#     }
#
#     spec = APISpec(
#         title=app.title,
#         version='1.0.0',
#         openapi_version='3.0.2',
#         plugins=[DataclassesPlugin()],
#     )
#
#     spec.path(
#         path='/test',
#         summary='This is Path Summary!',
#         description='This is Path Description!',
#         # operations={
#         #     'summary': 'This is the PathItem summary!',
#         #     'description': 'This is the PathItem description!',
#         #     'get': {
#         #         'tags': [{'name': 'tag1'}, {'name': 'tag2'}],
#         #         'summary': 'This is the Operation summary!',
#         #         'description': 'This is the Operation description!',
#         #         'operationId': 'This is the Operation operationId!',
#         #         'requestBody': {
#         #             'application/json': {}
#         #         }
#         #     }
#         # }
#     )
#
#     spec.components.schema(
#         component_id='MyModel',
#         schema=MyModel,
#     )
#
#     return spec.to_dict()
#
#     specs = OpenApi(
#         info=Info(
#             title=app.title,
#             version='0.1.0',
#         ),
#         paths={
#             '/test': PathItem(
#                 summary='This is the PathItem summary!',
#                 description='This is the PathItem description!',
#                 get=Operation(
#                     tags=[Tag(name='tag1'), Tag(name='tag2')],
#                     summary='This is the Operation summary!',
#                     description='This is the Operation description!',
#                     operationId='This is the Operation operationId!',
#                     requestBody=RequestBody(
#                         content={
#                             'application/json': MediaType(
#
#                             )
#                         }
#                     )
#                     # parameters=[
#                     #     Parameter(
#                     #         name='param1',
#                     #     ),
#                     #     Parameter(
#                     #         name='param2',
#                     #     ),
#                     # ],
#                 )
#             )
#         },
#         components=Components(
#             schemas={
#                 'HelloWorldComponent': Schema(
#
#                 )
#             },
#         )
#     )
#
#     return specs.as_dict()
#
#
# # import inspect
# # from typing import List, Dict, Any, Optional
# # from openapi_specgen import (
# #     OpenApi,
# #     OpenApiParam,
# #     OpenApiPath,
# #     OpenApiResponse,
# # )
# #
# # # from .app import Application
# # from .endpoint import Endpoint
# #
# # from dataclasses import dataclass, field
# # from typing import Optional, Union
# #
# #
# # class EndpointSpecs(object):
# #     """
# #     Generates OpenAPI specs based on an Application object.
# #     """
# #     def __init__(self, endpoint: Endpoint):
# #         self.endpoint = endpoint
# #
# #     @property
# #     def params(self) -> List[OpenApiParam]:
# #         return [OpenApiParam('param_name', 'query', data_type=str)]
# #
# #     @property
# #     def responses(self) -> List[OpenApiResponse]:
# #         return [OpenApiResponse(
# #             descr='Response description',
# #             data_type=int,
# #         )]
# #
# #
# # def generate_api_specs(app: 'Application') -> Dict[str, Any]:
# #     """
# #     :param app: Application
# #     :returns: OpenAPI specs
# #     """
# #     paths = []
# #
# #     for e in app.endpoints:
# #         response = OpenApiResponse(
# #             descr='Response description',
# #             data_type=int,
# #         )
# #
# #         # response = OpenApiResponse('Response description', data_type=int)
# #
# #         param = OpenApiParam('param_name', 'query', data_type=str)
# #
# #         path = OpenApiPath(
# #             path=e.path,
# #             descr=inspect.getdoc(e.endpoint),
# #             method=e.method.lower(),
# #             responses=[response],
# #             params=[param],
# #         )
# #
# #         paths.append(path)
# #
# #     return OpenApi(app.title, paths).as_dict()
