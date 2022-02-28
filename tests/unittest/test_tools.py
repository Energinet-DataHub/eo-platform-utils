import urllib.parse as urlparse

from src.origin.tools import url_append


def test__url_append__add_query_params__should_format_url_correctly():  # noqa: E501

    # -- Arrange -------------------------------------------------------------

    url = 'https://bacon.com/spam?foo=bar&bacon=spam'

    # -- Act -----------------------------------------------------------------

    return_url = url_append(
        url=url,
        query_extra={
            'foo': 'test',
            'cake': 'brownie',
        },
    )

    # -- Assert --------------------------------------------------------------

    return_url_parts = list(urlparse.urlparse(return_url))
    return_query = dict(urlparse.parse_qsl(return_url_parts[4]))

    assert return_url[:23] == 'https://bacon.com/spam?'
    assert return_query == {
        'foo': 'test',
        'cake': 'brownie',
        'bacon': 'spam',
    }


def test__url_append__add_path__should_format_url_correctly():

    # -- Arrange -------------------------------------------------------------

    url = 'https://bacon.com/spam?foo=bar&bacon=spam'

    # -- Act -----------------------------------------------------------------

    return_url = url_append(
        url=url,
        path_extra='/cake'
    )

    # -- Assert --------------------------------------------------------------

    assert return_url[:28] == 'https://bacon.com/spam/cake?'
