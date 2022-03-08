import pytest
from dataclasses import dataclass

from origin.bus import Message
from origin.serialize import \
    Serializer, simple_serializer, json_serializer


@dataclass
class Nested:
    """TODO."""

    something: str


@dataclass
class Message1(Message):
    """TODO."""

    something: str
    nested: Nested


class TestSerializer:
    """TODO."""

    @pytest.mark.parametrize('uut', [
        simple_serializer,
        json_serializer,
    ])
    def test__should_serialize_and_deserialize_correctly(

            self,
            uut: Serializer,
    ):
        """TODO."""

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        # -- Act -------------------------------------------------------------

        serialized = uut.serialize(obj=obj)
        deserialized = uut.deserialize(data=serialized, schema=Message1)

        # -- Assert ----------------------------------------------------------

        assert isinstance(deserialized, Message1)
        assert deserialized == obj
