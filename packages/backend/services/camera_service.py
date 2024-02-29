import cv2

def capture_continuous(frequency, file_path):
    cap = cv2.VideoCapture(0)  # 0 steht für die erste angeschlossene Kamera
    
    if not cap.isOpened():
        print("Kann Kamera nicht öffnen")
        return
    
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(file_path, frame)
        else:
            print("Kann Bild nicht erfassen")
            break
        
        # Wartezeit, um die gewünschte Frequenz zu erreichen
        cv2.waitKey(int(1000/frequency))

if __name__ == "__main__":
    capture_continuous(24, "/shared/web/captured_image.jpeg")
