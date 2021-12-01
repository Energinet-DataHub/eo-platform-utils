from dataclasses import dataclass, field
from typing import Optional, Union

from origin.api import Application, Endpoint


class OpenIdLogin(Endpoint):
    """
    Returns a URL which initiates a login flow @ the
    OpenID Connect Identity Provider.
    """

    @dataclass
    class Request:
        """
        This is the REQUEST!
        """
        return_url: str

    @dataclass
    class Response:
        """
        This is the RESPONSE!
        """
        url: Optional[str] = field(default=None)

    def handle_request(self, request: Request) -> Response:
        """
        Handle HTTP request.
        """
        return self.Response(url='url')


app = Application.create(
    title='Auth API',
    base_url='http://google.dk',
    secret='INTERNAL_TOKEN_SECRET',
    health_check_path='/health',
    docs_path='/docs',
)

# Login
# app.add_endpoint(
#     method='GET',
#     path='/docs',
#     endpoint=OpenApi(),
# )

# -- OpenID Connect Login ------------------------------------------------

# Login
app.add_endpoint(
    method='GET',
    path='/oidc/login',
    endpoint=OpenIdLogin(),
)

for e in app.endpoints:
    print(f'{e}')

j = 2
