# noqa
from fastapi import Depends, FastAPI, HTTPException, Header, Query, Request
import fastapi
from origin.api import Application, TokenGuard
from origin.api import Context, Endpoint
from dataclasses import dataclass, field


async def verify_token(request: Request, token: str = '1'):
    if token != '123':
        raise HTTPException(status_code=403, detail={'success': 'meh'})


class TestEndpoint(Endpoint):


    # dependencies = [Depends(verify_token)]

    @dataclass
    class Response:
        profile_name: str = field(
            default='bobbybob',
            metadata=dict(
                title='Username',
                description='This is the description',
            ),
        )

    def handle_request(
            self,
            name: str,
    ) -> Response:
        """
        Dank Docs.

        iasduijadsiuijnasd joadsjodasd onasddjo ipsum.
        """
        return self.Response(
            profile_name=name
        )


def create_app() -> Application:
    app = Application.create(
        name='Auth API',
        secret="",
        health_check_path='/health',
    )

    app.add_endpoint(
        method='GET',
        path='/something/{name}',
        endpoint=TestEndpoint(),
    )

    return app


# ------------------------------------
generic_app = create_app()


fastapi = generic_app._fast_api_app
app = FastAPI()

# app.add_api_route(
#     path='/something',
#     methods=['GET'],
#     endpoint=TestEndpoint().handle_request,
#     dependencies=[Depends(verify_token)]
# )
