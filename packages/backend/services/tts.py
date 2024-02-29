import os

from shared.mq.broker import Broker
from shared.mq.subscriber import Subscriber


def main():
    subscriber = Subscriber("tts", Broker.BACKEND_PORT)

    def speak(text: str) -> None:
        os.system("rm /tmp/output.wav")  # Remove the file if it exists
        os.system(
            f'pico2wave -w=/tmp/output.wav "..{text}.." && aplay /tmp/output.wav'
        )  # Create a new file and play it
        os.system("rm /tmp/output.wav")  # Remove the file after playing it

    while True:
        message = subscriber.subscribe()
        payload = message.payload
        if payload is not None:
            text = payload["text"]
            speak(text)


if __name__ == "__main__":
    try:
        print("Starting TTS service")
        main()
    except KeyboardInterrupt:
        print("Shutting down TTS service")
        exit(0)
