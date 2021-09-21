# from typing import Any, Optional
# from uuid import uuid4
# from datetime import datetime, timedelta
# from iterators import TimeoutIterator
#
# from energytt_platform.models.tech import \
#     Technology, TechnologyType
# from energytt_platform.bus import \
#     MessageBroker, Message, messages as m
#
#
# TOPIC = 'TEST-TOPIC'
# DEFAULT_TIMEOUT = 5
#
#
# class MessageHandlerMock(object):
#
#     class Timeout(Exception):
#         pass
#
#     def __init__(self):
#         self.invoked = False
#         self.msg = None
#
#     def __call__(self, msg: Any):
#         self.invoked = True
#         self.msg = msg
#
#     def wait(self, iterator, timeout: int = DEFAULT_TIMEOUT) -> Optional[Message]:
#         for self.msg in TimeoutIterator(iterator, timeout):
#             break
#
#         return self.msg
#
#     # def wait(self, timeout: int = DEFAULT_TIMEOUT) -> Optional[Message]:
#     #     begin = datetime.now()
#     #     delta = lambda: datetime.now() - begin
#     #
#     #
#     #
#     #     while (not self.invoked) and delta() < timedelta(seconds=timeout):
#     #         _delta = delta()
#     #         _continue = delta() < timedelta(seconds=timeout)
#     #         x = 2
#     #         pass
#     #
#     #     return self.msg
#
#
# class TestMessageBroker:
#     """
#     TODO
#     """
#
#     def test__provide_no_token__should_return_null(self, broker: MessageBroker):
#         """
#         TODO
#         """
#
#         handler = MessageHandlerMock()
#
#         msg_sent = m.TechnologyUpdate(
#             technology=Technology(
#                 tech_code=str(uuid4()),
#                 fuel_code=str(uuid4()),
#                 type=TechnologyType.solar,
#             )
#         )
#
#         broker.publish(
#             topic=TOPIC,
#             msg=msg_sent,
#         )
#
#         # broker.subscribe([TOPIC])
#
#         msg_received = MessageHandlerMock().wait(
#             iterator=broker.listen([TOPIC]),
#             timeout=5,
#         )
#
#         # loop = TimeoutIterator(
#         #     iterator=broker.listen([TOPIC]),
#         #     timeout=5.0,
#         # )
#         #
#         # for msg_received in loop:
#         #     # print(msg)
#         #     break
#
#         # msg_received = handler.wait()
#
#         assert msg_received == msg_sent
#
#         # message_received = False
#         #
#         # def on_message_received(message: Any):
#         #     message_received = True
#         #
#         # timeout = 10
#         # begin = datetime.now()
#         #
#         # for msg_received in broker.subscribe([TOPIC]):
#         #     assert msg_received == msg_sent
#         #     break
