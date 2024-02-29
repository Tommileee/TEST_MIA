import zmq

from .typings.message import Message


class Publisher:
    def __init__(self, broker_port: int = 5555) -> None:
        self.context = zmq.Context()

        # Initialize a publisher socket
        self.socket = self.context.socket(zmq.PUB)

        # Connect to the broker
        self.socket.connect(f"tcp://localhost:{broker_port}")

    def publish(self, message: Message) -> None:
        # Publish a message to the broker
        print(f"Publishing message: {message}")
        self.socket.send_string(message.encode())
