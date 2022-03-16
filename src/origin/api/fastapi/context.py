# from typing import Dict
# from fastapi import FastAPI, Request
# from functools import cached_property

# from origin.api.context import Context


# class FastAPIContext(Context):
#     """
#     FastAPI-specific context.
#     """

#     @cached_property
#     def headers(self) -> Dict[str, str]:
#         """
#         Handle the header.

#         :returns: HTTP request headers
#         """
#         return dict(request.headers)

#     @cached_property
#     def cookies(self) -> Dict[str, str]:
#         """
#         Handle the cookie.

#         :returns: HTTP request cookies
#         """
#         return request.cookies
