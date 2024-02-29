import cv2
import os

def capture_continuous(frequency, file_path):
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Kann Kamera nicht öffnen")
        return
    
    while True:
        ret, frame = cap.read()
        if ret:
            try:
                cv2.imwrite(file_path, frame)
                print("Bild gespeichert bei:", file_path)  # Bestätigung hinzugefügt
            except Exception as e:
                print("Fehler beim Speichern des Bildes:", e)
        else:
            print("Kann Bild nicht erfassen")

        cv2.waitKey(int(1000/frequency))

if __name__ == "__main__":
    # Stellen Sie sicher, dass der Pfad existiert oder fügen Sie Code hinzu, um ihn zu erstellen
    file_path = "/shared/web/captured_image.jpeg"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ordner erstellen, falls nicht vorhanden
    capture_continuous(24, file_path)
