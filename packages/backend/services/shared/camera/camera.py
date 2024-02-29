import io
import threading

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buffer):
        with self.condition:
            self.frame = buffer
            self.condition.notify_all()


class CameraStream:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(
            self.picam2.create_video_configuration(
                main={
                    "size": (640, 480),
                }
            )
        )
        self.output = StreamingOutput()
        self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))

    def get_frame(self):
        with self.output.condition:
            self.output.condition.wait()
            return self.output.frame

    def close(self):
        self.picam2.stop_recording()
        self.picam2.close()
