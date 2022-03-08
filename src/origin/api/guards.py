from typing import List
from abc import abstractmethod

from .context import Context
from .responses import Unauthorized


class EndpointGuard(object):
    """Only Allows requests with a valid endpoint provided."""

    @abstractmethod
    def validate(self, context: Context):
        """Validate the endpoint."""
        raise NotImplementedError


class TokenGuard(EndpointGuard):
    """Only Allows requests with a valid token provided."""

    def validate(self, context: Context):
        """Validate the token."""
        if context.token is None:
            raise Unauthorized('Unauthorized')


class ScopedGuard(EndpointGuard):
    """Only Allows requests with specific scopes granted."""

    def __init__(self, *scopes: str):
        self.scopes = scopes

    def validate(self, context: Context):
        """Validate the scope."""
        if context.token is None:
            raise Unauthorized('Unauthorized')
        for scope in self.scopes:
            if scope not in context.token.scope:
                # TODO Write proper message
                raise Unauthorized('Missing scope %s' % scope)


class Bouncer(object):
    """Class Bouncer to validate the context and the endpoints."""

    def validate(self, context: Context, guards: List[EndpointGuard]):
        """Validate the bouncer."""
        for guard in guards:
            guard.validate(context)


# -- Singletons --------------------------------------------------------------

bouncer = Bouncer()
