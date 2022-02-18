"""This module provides runtime support for type hints on dicts."""
from typing import Dict
from functools import cached_property
from fastapi.requests import Request

from origin.api.context import Context

class FastapiContext(Context):
    """
    Fastapi context
    """

    @cached_property
    def headers(self) -> Dict[str, str]:
        """
        :returns: HTTP request headers
        """
        return dict(Request.headers)

    @cached_property
    def cookies(self) -> Dict[str, str]:
        """
        :returns: HTTP request cookies
        """
        return dict(Request.cookies)
