# from dataclasses import dataclass
# from fastapi import Request as FastAPI_request
# from inspect import signature
# from inspect import getfullargspec
# from inspect import getmro

# @dataclass
# class Request:
#     """Response containing UserProfile on success."""
#     parm1: str
#     parm2: str

# def handle_request(
#         self,
#         request: Request,
# ) -> str:
#     return "sdsd"

# def handle_request_new(
#         self,
#         request: Request,
#         fastAPI_request: FastAPI_request,
# ) -> str:
#     return "sdsd"

# sig = signature(handle_request)
# parm = sig.parameters

# getmro(FastAPI_request)[0]



# t = FastAPI_request.__module__ + "." + FastAPI_request.__name__


# {
#     'request': <class 'tests.integrationtest.api.test_responses.TestEndpointResponse.test__fast_api__with_query_parms.<locals>.TestEndpoint.Request'>,
#     'return': <class 'tests.integrationtest.api.test_responses.TestEndpointResponse.test__fast_api__with_query_parms.<locals>.TestEndpoint.Response'>,
#     'fastAPI_request': <class 'starlette.requests.Request'>
# }

# {
#     'request': <class 'tests.integrationtest.api.test_responses.TestEndpointResponse.test__fast_api__with_query_parms.<locals>.TestEndpoint.Request'>,
#     'new_request': <class 'starlette.requests.Request'>,
#     'return': <class 'tests.integrationtest.api.test_responses.TestEndpointResponse.test__fast_api__with_query_parms.<locals>.TestEndpoint.Response'>,
#     'fastAPI_request': <class 'starlette.requests.Request'>
# }
