import cv2
import threading

class CameraStream:
    def __init__(self):
        # Initialisieren der Kamera
        self.capture = cv2.VideoCapture(0)  # 0 ist normalerweise die Standardkamera
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.frame = None
        self.running = True
        
        # Starten des Threads, um Kameraframes kontinuierlich zu lesen
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Lesen der Frames in einem separaten Thread
        while self.running:
            success, frame = self.capture.read()
            if success:
                self.frame = frame

    def get_frame(self):
        # Rückgabe des aktuellen Frames
        return self.frame

    def close(self):
        # Beenden des Frame-Lese-Threads und Freigabe der Kamera
        self.running = False
        self.thread.join()
        self.capture.release()
