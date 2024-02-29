from typing import Union

import zmq

from .typings.message import Message


class Subscriber:
    def __init__(self, topic: str, broker_port: int) -> None:
        self.topic = topic

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{broker_port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

    def _receive(self) -> Message:
        return Message.decode(self.socket.recv_string())

    def subscribe(self, timeout: Union[int, None] = None) -> Union[None, Message]:
        if timeout:
            try:
                if self.socket.poll(timeout):
                    return self._receive()
            except zmq.Again:
                return None
        else:
            return self._receive()
