# Standard Library
from typing import Dict, Optional

# Third party
from fastapi import Request

# First party
from origin.api.context import Context
from origin.models.auth import InternalToken
from origin.tokens import TokenEncoder


class FastAPIContext(Context):
    def __init__(self, request: Request):
        self.token_encoder = TokenEncoder(
            schema=InternalToken,
            secret='123',
        )
        self.request = request

    @cached_property
    def headers(self) -> Dict[str, str]:
        """
        Handle the header.

        :returns: HTTP request headers
        """
        return dict(self.request.headers)

    @cached_property
    def cookies(self) -> Dict[str, str]:
        """
        Handle the cookie.

        :returns: HTTP request cookies
        """
        return self.request.cookies
