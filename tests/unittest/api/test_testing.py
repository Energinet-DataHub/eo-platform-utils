import pytest
from typing import Optional

from energytt_platform.api.testing import (
    assert_base_url,
    assert_query_parameter,
)


class TestAssertBaseUrl:
    """
    Tests assert_base_url()
    """

    @pytest.mark.parametrize('check_path, url, expected_base_url', (
        (False, 'http://foobar.com', 'http://foobar.com'),
        (False, 'http://foobar.com/', 'http://foobar.com/'),
        (False, 'http://foobar.com/', 'http://foobar.com'),
        (False, 'http://foobar.com', 'http://foobar.com/'),
        (False, 'http://foobar.com', 'http://foobar.com/something'),
        (False, 'http://foobar.com', 'http://foobar.com/something?query=value'),  # noqa: E501
        (False, 'http://foobar.com', 'http://foobar.com/something?query=value#fragment'),  # noqa: E501
        (False, 'http://foobar.com/something', 'http://foobar.com'),
        (False, 'http://foobar.com/something?query=value', 'http://foobar.com'),  # noqa: E501
        (False, 'http://foobar.com/something?query=value#fragment', 'http://foobar.com'),  # noqa: E501
        (True, 'http://foobar.com', 'http://foobar.com'),
        (True, 'http://foobar.com/', 'http://foobar.com/'),
        (True, 'http://foobar.com/something', 'http://foobar.com/something'),
        (True, 'http://foobar.com/something', 'http://foobar.com/something?query=value'),  # noqa: E501
        (True, 'http://foobar.com/something', 'http://foobar.com/something?query=value#fragment'),  # noqa: E501
    ))
    def test__should_not_raise_assertion_error(
            self,
            check_path: bool,
            url: str,
            expected_base_url: str,
    ):
        """
        Only scheme and netloc should be identical. All other parts of
        the URL should be ignored.

        :param check_path: Whether or not to assert on the path-part also
        :param url: The URL to test
        :param expected_base_url: The base-URL to match
        """
        assert_base_url(
            url=url,
            expected_base_url=expected_base_url,
            check_path=check_path,
        )

    @pytest.mark.parametrize('check_path, url, expected_base_url', (
        (True, 'http://foobar.com/', 'http://foobar.com'),
        (True, 'http://foobar.com', 'http://foobar.com/'),
        (True, 'http://foobar.com/', 'http://foobar.com/something'),
        (True, 'http://foobar.com/', 'http://foobar.com;something'),
        (True, 'http://foobar.com/something', 'http://foobar.com'),
        (True, 'http://foobar.com;something', 'http://foobar.com'),
    ))
    def test__should_raise_assertion_error(
            self,
            check_path: bool,
            url: str,
            expected_base_url: str,
    ):
        """
        Note: Trailing slash is part of the path

        :param check_path: Whether or not to assert on the path-part also
        :param url: The URL to test
        :param expected_base_url: The base-URL to match
        """
        with pytest.raises(AssertionError):
            assert_base_url(
                url=url,
                expected_base_url=expected_base_url,
                check_path=True,
            )


class TestAssertQueryParameter:
    """
    Tests assert_query_parameter()
    """

    @pytest.mark.parametrize('url, name, value', (
        ('http://foobar.com?foo=bar', 'foo', None),
        ('http://foobar.com?foo=bar', 'foo', 'bar'),
        ('http://foobar.com?foo=bar&bar=foo', 'bar', None),
        ('http://foobar.com?foo=bar&bar=foo', 'bar', 'foo'),
    ))
    def test__should_not_raise_assertion_error(
            self,
            url: str,
            name: str,
            value: Optional[str],
    ):
        """
        Asserts the existence of a query parameter (by its name).

        :param url: The URL to test
        :param name: Name of the query parameter
        """
        assert_query_parameter(
            url=url,
            name=name,
        )

    @pytest.mark.parametrize('url, name, value', (
        ('http://foobar.com?foo=bar', 'bar', None),
        ('http://foobar.com?foo=bar', 'spam', None),
        ('http://foobar.com?foo=bar', 'foo', 'spam'),
        ('http://foobar.com?foo=bar', 'bar', 'foo'),
    ))
    def test__should_raise_assertion_error(
            self,
            url: str,
            name: str,
            value: Optional[str],
    ):
        """
        Asserts the existence of a query parameter (by its name).

        :param url: The URL to test
        :param name: Name of the query parameter
        """
        with pytest.raises(AssertionError):
            assert_query_parameter(
                url=url,
                name=name,
                value=value,
            )
