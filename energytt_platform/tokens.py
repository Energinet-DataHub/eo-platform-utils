import jwt
from typing import Generic, TypeVar, Type

from energytt_platform.serialize import simple_serializer


TToken = TypeVar('TToken')


class TokenEncoder(Generic[TToken]):
    """
    Generic helper-class to encode and decode dataclasses to and from JWT.
    """

    class EncodeError(Exception):
        """
        Raised when encoding fails.
        """
        pass

    class DecodeError(Exception):
        """
        Raised when decoding fails.
        """
        pass

    def __init__(self, cls_: Type[TToken], secret: str):
        self.cls = cls_
        self.secret = secret

    def encode(self, obj: TToken) -> str:
        """
        Encodes object to JWT.
        """
        payload = simple_serializer.serialize(
            obj=obj,
            cls=self.cls,
        )

        # TODO Raise EncodeError

        return jwt.encode(
            payload=payload,
            key=self.secret,
            algorithm='HS256',
        )

    def decode(self, encoded_jwt: str) -> TToken:
        """
        Decodes JWT to object.
        """
        payload = jwt.decode(
            jwt=encoded_jwt,
            key=self.secret,
            algorithms=['HS256'],
        )

        # TODO Raise DecodeError

        return simple_serializer.deserialize(
            data=payload,
            cls=self.cls,
        )
