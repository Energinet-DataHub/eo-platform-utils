import pytest
from datetime import datetime
from itertools import product
from wsgiref.headers import Headers
from flask.testing import FlaskClient
from http.cookies import SimpleCookie
from typing import Optional, Dict, Iterable, Any

from energytt_platform.api import Application, HttpResponse, Cookie

from .endpoints import EndpointReturnsGeneric


class CookieTester(object):
    """
    Helper for testing cookies in HTTP responses.
    """
    def __init__(self, headers: Headers):
        """
        :param headers:
        """
        self.cookies = SimpleCookie('\r\n'.join(headers.get_all('Set-Cookie')))

    def assert_has_cookies(self, *names: str) -> 'CookieTester':
        """
        Assert that exactly the specified cookies were set.

        :param names:
        """
        assert tuple(self.cookies.keys()) == names

        return self

    def assert_cookie(
            self,
            name: str,
            value: str,
            expires: Optional[datetime] = None,
            path: Optional[str] = None,
            comment: Optional[str] = None,
            domain: Optional[str] = None,
            max_age: Optional[str] = None,
            secure: Optional[bool] = None,
            http_only: Optional[bool] = None,
            version: Optional[str] = None,
            same_site: Optional[bool] = None,
    ) -> 'CookieTester':
        """
        Assert content of a cookie.

        :param name:
        :param value:
        :param expires:
        :param path:
        :param comment:
        :param domain:
        :param max_age:
        :param secure:
        :param http_only:
        :param version:
        :param same_site:
        :return:
        """
        assert self.cookies[name].value == value
        assert self.cookies[name]['expires'] == \
               (expires.strftime('%a, %d %b %Y %H:%M:%S GMT') if expires is not None else '')
        assert self.cookies[name]['path'] == (path if path is not None else '')
        assert self.cookies[name]['comment'] == (comment if comment is not None else '')
        assert self.cookies[name]['domain'] == (domain if domain is not None else '')
        assert self.cookies[name]['max-age'] == (max_age if max_age is not None else '')
        assert self.cookies[name]['secure'] == (secure if secure else '')
        assert self.cookies[name]['httponly'] == (http_only if http_only else '')
        assert self.cookies[name]['version'] == (version if version is not None else '')
        assert self.cookies[name]['samesite'] == ('Strict' if same_site else '')

        return self


def get_cookie_combinations() -> Iterable[Dict[str, Any]]:
    """
    TODO
    """

    combinations = product(
        (None, True, False),     # http_only
        (None, True, False),     # secure
        (None, True, False),     # same_site
        (None, 'domain.com'),    # domain
        (None, '/path'),         # path
        (None, datetime.now()),  # expires
    )

    for http_only, secure, same_site, domain, path, expires in combinations:
        yield {
            'name': 'Header1',
            'value': 'Value1',
            'http_only': http_only,
            'secure': secure,
            'same_site': same_site,
            'domain': domain,
            'path': path,
            'expires': expires,
        }


class TestCookies:

    @pytest.mark.parametrize('cookie_kwargs', get_cookie_combinations())
    def test__set_one_cookie__should_set_cookie_correctly(
            self,
            cookie_kwargs: Dict[str, Any],
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        response = HttpResponse(
            status=200,
            cookies=(Cookie(**cookie_kwargs),),
        )

        app.add_endpoint(
            method='GET',
            path='/something',
            endpoint=EndpointReturnsGeneric(response),
        )

        # -- Act -------------------------------------------------------------

        r = client.get('/something')

        # -- Assert ----------------------------------------------------------

        CookieTester(r.headers) \
            .assert_has_cookies(cookie_kwargs['name']) \
            .assert_cookie(**cookie_kwargs)

    def test__set_multiple_cookies__should_set_all_cookies_correctly(
            self,
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        response = HttpResponse(
            status=200,
            cookies=(
                Cookie(name='Cookie1', value='Value1'),
                Cookie(name='Cookie2', value='Value2'),
                Cookie(name='Cookie3', value='Value3'),
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

        CookieTester(r.headers) \
            .assert_has_cookies('Cookie1', 'Cookie2', 'Cookie3') \
            .assert_cookie(name='Cookie1', value='Value1') \
            .assert_cookie(name='Cookie2', value='Value2') \
            .assert_cookie(name='Cookie3', value='Value3')
