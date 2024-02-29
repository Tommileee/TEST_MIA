import cv2
import os

def capture_continuous(frequency):
    cap = cv2.VideoCapture(0)  # 0 steht für die erste angeschlossene Kamera

    if not cap.isOpened():
        print("Kann Kamera nicht öffnen")
        return

    # Ermitteln des Pfades zum aktuellen Skriptverzeichnis
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Zielverzeichnis relativ zum Skriptverzeichnis
    target_dir = os.path.join(current_dir, "shared", "web")

    # Stellen Sie sicher, dass das Zielverzeichnis existiert
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, "captured_image.jpeg")

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(file_path, frame)
            print(f"Bild gespeichert bei: {file_path}")
        else:
            print("Kann Bild nicht erfassen")

        # Wartezeit, um die gewünschte Frequenz zu erreichen
        cv2.waitKey(int(1000 / frequency))

if __name__ == "__main__":
    capture_continuous(24)
