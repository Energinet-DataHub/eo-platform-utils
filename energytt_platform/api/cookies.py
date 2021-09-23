from typing import Optional
from datetime import datetime
from http.cookies import SimpleCookie
from dataclasses import dataclass, field


@dataclass
class Cookie:
    """
    TODO Test this

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
    """
    name: str
    value: str
    http_only: bool = field(default=False)
    secure: bool = field(default=False)
    same_site: bool = field(default=False)
    domain: Optional[str] = field(default=None)
    path: Optional[str] = field(default=None)
    expires: Optional[datetime] = field(default=None)

    def __str__(self) -> str:
        c = SimpleCookie()
        c[self.name] = self.value

        return str(c)


if __name__ == '__main__':
    c = Cookie(
        name='Location',
        value='http://john.com',
    )

    print(str(c))
