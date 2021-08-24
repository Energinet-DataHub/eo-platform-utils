import jwt
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from energytt_platform.serialize import Serializable, simple_serializer


# @dataclass
# class GarbageToken(Serializable):
#     issued: datetime
#     expires: datetime
#     subject: str
#     scope: List[str]
#     on_behalf_of: Optional[str]
#
#     @property
#     def actual_subject(self) -> str:
#         if self.on_behalf_of:
#             return self.on_behalf_of
#         else:
#             return self.subject


# Temporary secret placed here
SYSTEM_SECRET = 'foobar'


@dataclass
class OpaqueToken(Serializable):
    issued: datetime
    expires: datetime
    subject: str
    scope: List[str]
    on_behalf_of: Optional[str]

    @property
    def actual_subject(self) -> str:
        if self.on_behalf_of:
            return self.on_behalf_of
        else:
            return self.subject


# TODO "from tokens import TokenEncoder" etc...


def encode_opaque_token(token: OpaqueToken) -> str:
    return jwt.encode(
        payload=simple_serializer.serialize(token),
        key=SYSTEM_SECRET,
        algorithm='HS256',
    )


def decode_opaque_token(encoded_jwt: str) -> OpaqueToken:
    decoded_jwt = jwt.decode(
        jwt=encoded_jwt,
        key=SYSTEM_SECRET,
        algorithms=['HS256'],
    )

    opaque_token = simple_serializer.deserialize(
        data=decoded_jwt,
        cls=OpaqueToken,
    )

    return opaque_token
