import datetime
import ipaddress
import json
import os
import ssl
import tempfile
from datetime import timezone
import cv2
import numpy as np
import time
 
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.websocket
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.x509.oid import NameOID
from shared.arduino.arduino import Arduino
from shared.arduino.driving.advanced import advanced_driving_algorithm
from shared.arduino.driving.simple import simple_driving_algorithm
from shared.arduino.targets import Target as ArduinoTargets
from shared.mq.publisher import Publisher
from shared.camera.camera import UsbCamera
from shared.mq.typings.message import Message
from tornado.process import cpu_count
 
 
import tornado
import tornado.web
import tornado.gen
import cv2
 
publisher = Publisher()
arduino = Arduino()
cam = None
 
class StreamHandler(tornado.web.RequestHandler):
    async def get(self):
        ioloop = tornado.ioloop.IOLoop.current()
 
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header( 'Pragma', 'no-cache')
        self.set_header( 'Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')
 
        self.served_image_timestamp = time.time()
        my_boundary = "--jpgboundary"
        while True:
            # Generating images for mjpeg stream and wraps them into http resp
            if self.get_argument('fd') == "true":
                img = cam.get_frame(True)
            else:
                img = cam.get_frame(False)
            interval = 0.1
            if self.served_image_timestamp + interval < time.time():
                self.write(my_boundary)
                self.write("Content-type: image/jpeg\r\n")
                self.write("Content-length: %s\r\n\r\n" % len(img))
                self.write(img)
                self.served_image_timestamp = time.time()
                await self.flush()
 
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
 
    def options(self, *args):
        self.set_header("Access-Control-Allow-Methods", "*")
        self.set_header("Access-Control-Request-Credentials", "true")
        self.set_header("Access-Control-Allow-Private-Network", "true")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_status(204)  # No Content
 
class DrivingAdvancedHandler(BaseHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body)
            motor_left = data.get("motor_left")
            motor_right = data.get("motor_right")
            client_now = data.get("now")
            utc_now = datetime.datetime.now(timezone.utc)
            unix_timestamp = utc_now.timestamp()
 
            latency = unix_timestamp - client_now
 
            print(f"Received driving advanced request with latency: {latency}")
 
            motor_left, motor_right = await tornado.ioloop.IOLoop.current().run_in_executor(
                None, advanced_driving_algorithm, motor_left, motor_right)
 
            arduino.send(ArduinoTargets.MOTOR_LEFT, motor_left)
            arduino.send(ArduinoTargets.MOTOR_RIGHT, motor_right)
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"error": "Invalid JSON"})
 
class DrivingSimpleHandler(BaseHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body)
            speed = data.get("speed")
            direction = data.get("direction")
            client_now = data.get("now")
            utc_now = datetime.datetime.now(timezone.utc)
            unix_timestamp = utc_now.timestamp()
 
            latency = unix_timestamp - client_now
 
            print(f"Received driving simple request with latency: {latency}")
 
            motor_left, motor_right = await tornado.ioloop.IOLoop.current().run_in_executor(
                None, simple_driving_algorithm, speed, direction)
 
            arduino.send(ArduinoTargets.MOTOR_LEFT, motor_left)
            arduino.send(ArduinoTargets.MOTOR_RIGHT, motor_right)
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"error": "Invalid JSON"})
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
 
    async def on_message(self, message):
        json = tornado.escape.json_decode(message)
 
        topic = json["topic"]
        payload = json["payload"]
 
        print(f"Received message: {topic} {payload}")
 
        # Process messages asynchronously to prevent blocking
        if topic == "tts":
            publisher.publish(Message("TTS", {"text": payload}))
        elif topic == "ai":
            publisher.publish(Message("AI", {"state": "trigger-recording"}))
        elif topic == "driving-advanced":
            motor_left = payload["motor_left"]
            motor_right = payload["motor_right"]
 
            motor_left, motor_right = await tornado.ioloop.IOLoop.current().run_in_executor(
                None, advanced_driving_algorithm, motor_left, motor_right)
 
            arduino.send(ArduinoTargets.MOTOR_LEFT, motor_left)
            arduino.send(ArduinoTargets.MOTOR_RIGHT, motor_right)
        elif topic == "driving-simple":
            speed = payload["speed"]
            direction = payload["direction"]
 
            left_motor, right_motor = await tornado.ioloop.IOLoop.current().run_in_executor(
                None, simple_driving_algorithm, speed, direction)
 
            arduino.send(ArduinoTargets.MOTOR_LEFT, left_motor)
            arduino.send(ArduinoTargets.MOTOR_RIGHT, right_motor)
 
def make_app():
    return tornado.web.Application([
        (r"/api/driving-advanced", DrivingAdvancedHandler),
        (r"/api/driving-simple", DrivingSimpleHandler),
        (r"/websocket", WebSocketHandler),
        (r'/video_feed', StreamHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "shared/web")}),
    ])
 
def generate_adhoc_ssl_pair(cn="localhost", san=None):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
 
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])
 
    alt_names = [x509.DNSName(cn)]
    if san:
        alt_names.extend([x509.IPAddress(ipaddress.ip_address(san))])
 
    san_extension = x509.SubjectAlternativeName(alt_names)
 
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=365))
            .add_extension(san_extension, critical=False)
            .sign(key, hashes.SHA256()))
 
    return cert, key
 
if __name__ == "__main__":
    cam = UsbCamera()
    app = make_app()
 
    cert, key = generate_adhoc_ssl_pair(san="127.0.0.1")
    cert_pem = cert.public_bytes(Encoding.PEM)
    key_pem = key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption())
    with tempfile.NamedTemporaryFile(delete=False) as cert_file, tempfile.NamedTemporaryFile(delete=False) as key_file:
        cert_file.write(cert_pem)
        key_file.write(key_pem)
        cert_file_path = cert_file.name
        key_file_path = key_file.name
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(certfile=cert_file_path, keyfile=key_file_path)
 
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
    server.listen(1606)  # Bind to port 8888 or any other port you prefer
    #server.start(0)  # Automatically start the same number of processes as cores available
    tornado.ioloop.IOLoop.current().start()
    os.unlink(cert_file_path)
    os.unlink(key_file_path)