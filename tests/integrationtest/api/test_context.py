from flask.testing import FlaskClient

from energytt_platform.api import Application
from energytt_platform.models.auth import InternalToken
from energytt_platform.tokens import TokenEncoder

from .endpoints import (
    EndpointRequiresContextReturnsToken,
)


class TestContext:
    """
    TODO
    """

    def test__provide_no_token__should_return_null(
            self,
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EndpointRequiresContextReturnsToken(),
        )

        # -- Act -------------------------------------------------------------

        r = client.post('/something')

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 200
        assert r.json == {'token': None}

    def test__provide_valid_token__should_return_token_as_json(
            self,
            app: Application,
            client: FlaskClient,
            valid_token: InternalToken,
            token_encoder: TokenEncoder[InternalToken],
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EndpointRequiresContextReturnsToken(),
        )

        token_encoded = token_encoder.encode(valid_token)

        # -- Act -------------------------------------------------------------

        r = client.post(
            path='/something',
            headers={'Authorization': f'Bearer: {token_encoded}'},
        )

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 200
        assert r.json == {
            'token': {
                'issued': valid_token.issued.isoformat(),
                'expires': valid_token.expires.isoformat(),
                'actor': valid_token.actor,
                'subject': valid_token.subject,
                'scope': valid_token.scope,
            },
        }
