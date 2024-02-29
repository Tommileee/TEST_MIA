import cv2
import time

def capture_and_save_image(frequency, duration, file_path):
    # Initialisiere die Kamera
    cap = cv2.VideoCapture(0)  # 0 steht für die erste angeschlossene Kamera

    if not cap.isOpened():
        print("Kann Kamera nicht öffnen")
        return

    start_time = time.time()
    end_time = start_time + duration
    interval = 1 / frequency

    while time.time() < end_time:
        ret, frame = cap.read()
        if ret:
            # Bild speichern
            cv2.imwrite(file_path, frame)
        else:
            print("Kann Bild nicht erfassen")
            break
        
        # Warte, um die Frequenz von 24 Bildern pro Sekunde zu erreichen
        time.sleep(interval)

    # Ressourcen freigeben
    cap.release()
    cv2.destroyAllWindows()

# Legen Sie die Frequenz der Bildaufnahme (24 Bilder pro Sekunde),
# die Dauer der Bildaufnahme in Sekunden und den Pfad der Datei fest
frequency = 24  # Bilder pro Sekunde
duration = 10   # Dauer in Sekunden, für wie lange Bilder aufgenommen werden sollen
file_path = "/shared/web/captured_image.jpeg"  # Pfad, wo das Bild gespeichert wird

capture_and_save_image(frequency, duration, file_path)
