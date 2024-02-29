import json


class Message:
    def __init__(self, topic: str, payload: dict) -> None:
        self.topic = topic
        self.payload = payload

    def encode(self) -> str:
        return f"{self.topic} {json.dumps(self.payload)}"

    def __str__(self) -> str:
        return self.encode()

    @staticmethod
    def decode(message: str) -> "Message":
        topic, payload = message.split(" ", 1)
        return Message(topic, json.loads(payload))
