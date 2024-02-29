def simple_driving_algorithm(speed: int, direction: int):
    """Simple driving algorithm for the Arduino to control the chain drive motors.
    Args:
        speed (int): The speed of the motors. (-255 to 255)
        direction (int): The direction of the motors. (-255 to 255)
    """

    motor_left = 0
    motor_right = 0

    # Berechnung der Motorwerte basierend auf der Geschwindigkeit und Lenkung
    if speed == 0:
        # Wenn keine Geschwindigkeit, basiere die Motorwerte nur auf der Lenkung
        if direction > 0:
            motor_right = direction
            motor_left = -direction
        else:
            motor_right = direction
            motor_left = -direction
    else:
        # Wenn Geschwindigkeit vorhanden ist, kombiniere Geschwindigkeit und Lenkung
        motor_right = speed - (direction / 2)
        motor_left = speed + (direction / 2)

    # Begrenze die Motorwerte auf den Bereich -255 bis 255
    motor_right = max(min(motor_right, 255), -255)
    motor_left = max(min(motor_left, 255), -255)

    return int(motor_left), int(motor_right)
