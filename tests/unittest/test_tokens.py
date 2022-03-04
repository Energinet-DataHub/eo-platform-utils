from dataclasses import dataclass

import jwt
import pytest
import json
import base64

from origin.bus import Message
from origin.tokens import TokenEncoder


@dataclass
class Nested:
    something: str


@dataclass
class MockMessage(Message):
    something: str
    nested: Nested


class TestTokenEncoder:

    @pytest.mark.unittest
    def test__should_encode_and_decode_correctly(self):

        # -- Arrange ---------------------------------------------------------

        obj = MockMessage(
            something='something',
            nested=Nested(something='something nested'),
        )

        uut = TokenEncoder(
            schema=MockMessage,
            secret='123',
        )

        # -- Act -------------------------------------------------------------

        encoded = uut.encode(obj=obj)
        decoded = uut.decode(encoded_jwt=encoded)

        # -- Assert ----------------------------------------------------------

        assert isinstance(decoded, MockMessage)
        assert decoded != encoded
        assert decoded == obj

    def test__encode_with_invalid_secret__should_fail_to_decode(self):

        # -- Arrange ---------------------------------------------------------

        obj = MockMessage(
            something='something',
            nested=Nested(something='something nested'),
        )

        uut = TokenEncoder(
            schema=MockMessage,
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

        # Reencrypt token with invalid secret
        new_encoded = jwt.encode(
            raw_decoded_token,
            "invalid-secret-key",
            algorithm=TokenEncoder.HS256,
        )

        # -- Assert ----------------------------------------------------------

        with pytest.raises(TokenEncoder.DecodeError):
            uut.decode(encoded_jwt=new_encoded)

    def test__tamper_with_token_payload__should_fail_to_decode(self):
        """
        Modify JWT token payload without changing signature expect to fail.

        Test that modifying the JWT token payload without changing the
        signature. This should result in an error, since the signature
        does not match up.
        """

        # -- Arrange ---------------------------------------------------------

        obj = MockMessage(
            something='something',
            nested=Nested(something='something nested'),
        )

        uut = TokenEncoder(
            schema=MockMessage,
            secret='123',
            alg=TokenEncoder.HS256,
        )

        encoded = uut.encode(obj=obj)

        # -- Act -------------------------------------------------------------

        # Split up up token in header, payload and signatur
        jwt_splitted = encoded.split('.')

        # Grab payload
        jwt_payload_encoded = jwt_splitted[1]

        # Add padding (required for base64)
        jwt_payload_encoded += "=" * ((4 - len(jwt_payload_encoded) % 4) % 4)

        jwt_payload_decoded = base64.b64decode(jwt_payload_encoded) \
            .decode("utf-8")

        # Load and modify json
        json_object = json.loads(jwt_payload_decoded)
        json_object['something'] = 'something123'

        # Convert to bytes
        modified_payload = json.dumps(json_object).encode('ascii')

        # base64 encode and remove '=' not needed in the jwt standard
        modified_payload_encoded = \
            base64.b64encode(modified_payload) \
            .decode('ascii') \
            .replace('=', '')

        # Assemble token with original header and signature.
        modified_token = '.'.join([
            jwt_splitted[0],
            modified_payload_encoded,
            jwt_splitted[2]
        ])

        # -- Assert ----------------------------------------------------------

        with pytest.raises(TokenEncoder.DecodeError):
            uut.decode(encoded_jwt=modified_token)
