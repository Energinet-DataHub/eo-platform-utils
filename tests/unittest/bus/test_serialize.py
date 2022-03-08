import pytest
from dataclasses import dataclass
from mock import MagicMock, patch

from origin.bus import Message
from origin.bus.serialize import MessageSerializer


@dataclass
class Nested:
    """Class to store the parameter for a nested message."""

    something: str


@dataclass
class Message1(Message):
    """Class to store the parameters for the message."""

    something: str
    nested: Nested


class TestMessageSerializer:
    """Class to test the serialize and deserialize functions."""

    def test__should_serialize_and_deserialize_correctly(self):
        """
        Tests if the serialize and deserialize functions work correctly.

        If the message is serialized and deserialized correctly, the test will
        pass.
        """

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        registry_mock = MagicMock()
        registry_mock.__contains__.return_value = True
        registry_mock.get.return_value = Message1

        uut = MessageSerializer(registry=registry_mock)

        # -- Act -------------------------------------------------------------

        serialized = uut.serialize(obj)
        deserialized = uut.deserialize(serialized)

        # -- Assert ----------------------------------------------------------

        assert isinstance(deserialized, Message1)
        assert deserialized == obj
        assert deserialized != serialized

    def test__serialize__message_not_in_registry__should_raise_serialize_error(self):  # noqa: E501
        """
        Tests if the serialize function raises error.

        If the message is not in the registry an error should be raised.
        """
        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        registry_mock = MagicMock()
        registry_mock.__contains__.return_value = False

        uut = MessageSerializer(registry=registry_mock)

        # -- Act -------------------------------------------------------------

        with pytest.raises(uut.SerializeError):
            uut.serialize(obj)

    @patch('origin.bus.serialize.json_serializer')
    def test__deserialize__message_not_in_registry__should_raise_deserialize_error(  # noqa: E501
            self,
            json_serializer_mock,
    ):
        """
        Tests if the deserialize function raises error.

        If the message is not in the registry an error should be raised.
        """

        # -- Arrange ---------------------------------------------------------

        registry_mock = MagicMock()
        registry_mock.__contains__.return_value = False

        wrapped_msg_mock = MagicMock(type=123)

        json_serializer_mock.deserialize.return_value = wrapped_msg_mock

        uut = MessageSerializer(registry=registry_mock)

        # -- Act -------------------------------------------------------------

        with pytest.raises(uut.DeserializeError):
            uut.deserialize(b'does not matter')
