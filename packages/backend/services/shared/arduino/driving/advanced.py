def advanced_driving_algorithm(left_speed: int, right_speed: int):
    """Advanced driving algorithm for the Arduino to directly control the chain drive motors.
    Args:
        left_speed (int): The speed of the left motor. (-255 to 255)
        right_speed (int): The speed of the right motor. (-255 to 255)
    """

    # Normalize the speed to be between -255 and 255
    left_speed = max(-255, min(255, left_speed))
    right_speed = max(-255, min(255, right_speed))

    return left_speed, right_speed
