from http.cookies import SimpleCookie

from flask.testing import FlaskClient

from energytt_platform.api import Application, HttpResponse, Cookie

from .endpoints import EndpointReturnsGeneric


class TestCookies:

    def test__endpoint_returns_redirect(
            self,
            app: Application,
            client: FlaskClient,
    ):

        # -- Arrange ---------------------------------------------------------

        response = HttpResponse(
            status=200,
            cookies=(
                Cookie(name='Header1', value='Value1'),
                Cookie(name='Header2', value='Value2'),
            ),
        )

        app.add_endpoint(
            method='GET',
            path='/something',
            endpoint=EndpointReturnsGeneric(response),
        )

        # -- Act -------------------------------------------------------------

        r = client.get('/something')

        # -- Assert ----------------------------------------------------------

        cookies = SimpleCookie('\r\n'.join(r.headers.get_all('Set-Cookie')))

        assert r.status_code == 200
        assert cookies['Header1'].value == 'Value1'
        assert cookies['Header2'].value == 'Value2'
