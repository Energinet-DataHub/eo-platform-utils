from typing import Dict, Type

from .broker import TMessage, TMessageHandler


def dispatch(handlers: Dict[Type[TMessage], TMessageHandler]) -> TMessageHandler:

    def _dispatch(msg: TMessage):
        if type(msg) in handlers:
            handler = handlers[type(msg)]
            handler(msg)

    return _dispatch
