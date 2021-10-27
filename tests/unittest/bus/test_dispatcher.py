from unittest.mock import Mock
from dataclasses import dataclass

from energytt_platform.bus.dispatcher import MessageDispatcher

from energytt_platform.bus import Message


@dataclass
class Message1(Message):
    something: str


@dataclass
class Message2(Message):
    something: str


class TestMessageSerializer:

    def test__handler_exists_for_type__should_invoke_handler(self):

        # -- Arrange ---------------------------------------------------------

        msg = Message1(something='something')

        handler1 = Mock()
        handler2 = Mock()

        uut = MessageDispatcher({
            Message1: handler1,
            Message2: handler2,
        })

        # -- Act -------------------------------------------------------------

        uut(msg)

        # -- Assert ----------------------------------------------------------

        handler1.assert_called_once_with(msg)
        handler2.assert_not_called()

    def test__handler_does_not_exist_for_type__should_not_invoke_handler(self):

        # -- Arrange ---------------------------------------------------------

        handler = Mock()

        uut = MessageDispatcher({
            Message1: handler,
        })

        # -- Act -------------------------------------------------------------

        uut(Message2(something='something'))

        # -- Assert ----------------------------------------------------------

        handler.assert_not_called()
