import time

import serial
import serial.tools.list_ports


class Arduino:
    __BAUD_RATE = 9600
    __MAX_CHARACTERS_PER_SECOND = (__BAUD_RATE / 10) - (
        __BAUD_RATE * 0.01
    )  # 10% of the baud rate, minus 1% for safety
    __connection = None

    CHARACTERS_SENT = 0
    START_TIME = time.time()

    def __init__(self) -> None:
        self.__setup_serial_connection()

        if self.__connection is None:
            print("No Arduino found")

    def __setup_serial_connection(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino" in port.manufacturer:
                self.__connection = serial.Serial(
                    port.device, self.__BAUD_RATE, write_timeout=0
                )

    def send(self, target: str, value: int):
        message = f"{target} {value}\n"

        Arduino.CHARACTERS_SENT += len(message)

        if Arduino.meanCharactersPerSecond() > self.__MAX_CHARACTERS_PER_SECOND:
            # Wait for the Arduino to catch up
            time.sleep(3)
            raise Exception("Arduino is being overloaded! Slow down the messages!")

        try:
            self.__connection.write(message.encode())
        except Exception:
            print("Could not send data to Arduino")
            print(f"Payload: {target} {value}")

    @staticmethod
    def meanCharactersPerSecond():
        return Arduino.CHARACTERS_SENT / (time.time() - Arduino.START_TIME)
