#include <Arduino.h>

int MOTOR_LEFT_DIRECTION = 12;
int MOTOR_LEFT_SPEED = 3;
int MOTOR_RIGHT_DIRECTION = 13;
int MOTOR_RIGHT_SPEED = 11;

int MOTOR_LEFT_BACKWARDS = HIGH;
int MOTOR_RIGHT_BACKWARDS = LOW;
int MOTOR_LEFT_FORWARDS = LOW;
int MOTOR_RIGHT_FORWARDS = HIGH;

void setup() {
    Serial.begin(9600);

    pinMode(MOTOR_LEFT_SPEED, OUTPUT);
    pinMode(MOTOR_RIGHT_SPEED, OUTPUT);
    pinMode(MOTOR_LEFT_DIRECTION, OUTPUT);
    pinMode(MOTOR_RIGHT_DIRECTION, OUTPUT);
}

void loop() {
    if(Serial.available()) {
        const String input = Serial.readStringUntil('\n');
        const int command_end_index = input.indexOf(" ");
        String command = input.substring(0, command_end_index);
        int value = input.substring(command_end_index, input.length()).toInt();

        Serial.println(value);

        command.toLowerCase();
        command.trim();

        if(command == "motor-left") {
            int direction = MOTOR_LEFT_FORWARDS;

            if(value < 0) {
                direction = MOTOR_LEFT_BACKWARDS;
                value *= -1;
            }

            digitalWrite(MOTOR_LEFT_DIRECTION, direction);
            analogWrite(MOTOR_LEFT_SPEED, value);
        } else if(command == "motor-right") {
            int direction = MOTOR_RIGHT_FORWARDS;

            if(value < 0) {
                direction = MOTOR_RIGHT_BACKWARDS;
                value *= -1;
            }

            digitalWrite(MOTOR_RIGHT_DIRECTION, direction);
            analogWrite(MOTOR_RIGHT_SPEED, value);
        } else if(command == "arm-left") {
            //TODO: Implement me
            // Servos sind nicht stark genug um Arme zu heben, daher ist keine
            // Implementierung notwendig.
        } else if (command == "arm-right") {
            //TODO: Implement me
            // Servos sind nicht stark genug um Arme zu heben, daher ist keine
            // Implementierung notwendig.
        } else if(command == "head-extension") {
            //TODO: Implement me
            // Noch nicht verbunden.
        } else if(command == "head-rotation") {
            //TODO: Implement me
            // Noch nicht verbunden.
        }
    }
}