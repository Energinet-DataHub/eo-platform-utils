from dataclasses import dataclass

import jwt
import pytest

from origin.bus import Message
from origin.tokens import TokenEncoder


@dataclass
class Nested:
    something: str


@dataclass
class Message1(Message):
    something: str
    nested: Nested


class TestTokenEncoder:

    def test__should_encode_and_decode_correctly(self):

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        uut = TokenEncoder(
            schema=Message1,
            secret='123',
        )

        # -- Act -------------------------------------------------------------

        encoded = uut.encode(obj=obj)
        decoded = uut.decode(encoded_jwt=encoded)

        # -- Assert ----------------------------------------------------------

        assert isinstance(decoded, Message1)
        assert decoded != encoded
        assert decoded == obj

    def test__tamper_with_token_payload__should_fail_to_decode(self):

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        uut = TokenEncoder(
            schema=Message1,
            secret='123',
            alg=TokenEncoder.HS256,
        )

        # -- Act -------------------------------------------------------------

        encoded = uut.encode(obj=obj)

        # Decode token
        raw_decoded_token = jwt.decode(
            encoded,
            "secret",
            algorithms=[TokenEncoder.HS256],
            options={"verify_signature": False}
        )

        # Update payload
        raw_decoded_token['something'] = 'something else'

        # Reencrypt token with invalid secret
        new_encoded = jwt.encode(
            raw_decoded_token,
            "invalid-secret-key",
            algorithm=TokenEncoder.HS256,
        )

        # -- Assert ----------------------------------------------------------

        with pytest.raises(TokenEncoder.DecodeError):
            uut.decode(encoded_jwt=new_encoded)
