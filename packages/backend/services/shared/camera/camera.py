import cv2
import numpy as np

class UsbCamera(object):
    """ Init camera """

    def __init__(self):
        # select first video device in system
        self.cam = cv2.VideoCapture(0)
        # set camera resolution to 480p
        self.w = 640  # Width
        self.h = 480  # Height
        # set camera to 30 FPS
        self.cam.set(cv2.CAP_PROP_FPS, 30)
        # apply new resolution
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
        # load cascade file for face detection
        self.face_cascade = cv2.CascadeClassifier('face.xml')

    def set_resolution(self, new_w, new_h):
        """
        Change camera resolution
        inputs: new_w, new_h - width and height of picture, must be int
        """
        if isinstance(new_h, int) and isinstance(new_w, int):
            # check if args are int and correct
            if (new_w <= 800) and (new_h <= 600) and (new_w > 0) and (new_h > 0):
                self.w = new_w
                self.h = new_h
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
            else:
                # bad params
                raise Exception('Bad resolution')
        else:
            # bad params
            raise Exception('Not int value')

    def get_frame(self, fdenable):
        """
        Gets frame from camera and tries to find faces on it
        :return: byte array of jpeg encoded camera frame
        """
        success, image = self.cam.read()
        if success:
            # scale image
            image = cv2.resize(image, (self.w, self.h))
            if fdenable:
                # resize image for speeding up recognize
                gray = cv2.resize(image, (320, 240))
                # make it grayscale
                gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
                # face cascade detector
                faces = self.face_cascade.detectMultiScale(gray)
                # draw rect on face areas
                scale = float(self.w / 320.0)
                count = 0
                for f in faces:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    x, y, z, t = [int(float(v) * scale) for v in f]
                    cv2.putText(image, str(x) + ' ' + str(y), (0, (self.h - 10 - 25 * count)), font, 1, (0, 0, 0), 2)
                    count += 1
                    cv2.rectangle(image, (x, y), (x + z, y + t), (255, 255, 255), 2)
        else:
            image = np.zeros((self.h, self.w, 3), np.uint8)
            cv2.putText(image, 'No camera', (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        # encoding picture to jpeg
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

# Beispiel zur Verwendung der Klasse:
if __name__ == "__main__":
    camera = UsbCamera()
    # Aktivieren Sie den folgenden Code, um eine Frame zu erhalten (hier nur als Beispiel, da dies in einer Schleife erfolgen sollte)
    # frame = camera.get_frame(fdenable=True)
    # Hier müssten Sie den Frame weiterverarbeiten, z.B. anzeigen oder speichern
