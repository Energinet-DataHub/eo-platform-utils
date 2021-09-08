from datetime import datetime
from unittest.mock import Mock

from energytt_platform.bus import messages as m
from energytt_platform.bus.dispatcher import MessageDispatcher


from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.models.common import DateTimeRange
from energytt_platform.models.measurements import Measurement


@dataclass
class TestMessage1(Message):
    something: str


@dataclass
class TestMessage2(Message):
    something: str


class TestMessageSerializer:

    def test__handler_exists_for_type__should_invoke_handler(self):

        # -- Arrange ---------------------------------------------------------

        msg = TestMessage1(something='something')

        handler = Mock()

        uut = MessageDispatcher({
            TestMessage1: handler,
        })

        # -- Act -------------------------------------------------------------

        uut(msg)

        # -- Assert ----------------------------------------------------------

        handler.assert_called_once_with(msg)

    def test__handler_does_not_exist_for_type__should_not_invoke_handler(self):

        # -- Arrange ---------------------------------------------------------

        handler = Mock()

        uut = MessageDispatcher({
            TestMessage1: handler,
        })

        # -- Act -------------------------------------------------------------

        uut(TestMessage2(something='something'))

        # -- Assert ----------------------------------------------------------

        handler.assert_not_called()
