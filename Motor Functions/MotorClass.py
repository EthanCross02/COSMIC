"""
This script will be used to collect the classes, therefore functions
of every motor control.

Please be sure to comment liberally for each motor control so that it is always clear
on what you are trying to accomplish. It might be worth looking into python commenting standards
to keep everything clean. Please reach out to Ethan if you need any assistance.

The plan should be to create a master class that is 'Motor' that will house the GPIO
input and output variables so that we do not have to continue to reinitialize the class.
All other motor classes can be created as a subclass of 'Motor'.
"""
from unittest import case

import RPi.GPIO as GPIO
from typing import Final
import time

NEUTRAL: Final[int] = 0 #this is an assumption on servo neutral position
SPEED: Final[int] = ...

GPIO.setmode(GPIO.BOARD)

def servo_setting(position: str) -> int:
    """Function that will be called to for servo settings"""
    match position:
        case "UP":
            return 90
        case "DOWN":
            return -90
        case "CENTER":
            return 0
        case _:  # Default case (handles invalid input)
            raise ValueError(f"Invalid position: {position}")


class Motor:
    """
    This class defines all motors used in the project.

    It should be used as a parent class where other motors will be subclasses of 'Motor'.
    """

    def __init__(self, out_pin1: int, out_pin2: int=None, out_pin3: int=None):
        """
        Constructor method to initialize the motor.

        :param out_pin: GPIO pin number assigned to the motor output.
        """
        self.output1 = out_pin1
        GPIO.setup(self.output1, GPIO.OUT)  # Configure pin as output

        if out_pin2 is not None:
            self.output2 = out_pin2
            GPIO.setup(self.output2, GPIO.OUT)
        else:
            self.output2 = None

        if out_pin3 is not None:
            self.output3 = out_pin3
            GPIO.setup(self.output3, GPIO.OUT)
        else:
            self.output3 = None

class ServoMotor(Motor):
    def __init__(self, pwm_pin: int):
        super().__init__(pwm_pin)
        self.pwm_pin = pwm_pin
        self.pwm = GPIO.PWM(self.pwm_pin, 50)
        self.pwm.start(NEUTRAL)

    def change_pos(self, position: str):
        """Method to change the position of as servo"""
        state = servo_setting(position)
        self.pwm.ChangeDutyCycle(state)

class DCMotor(Motor):
    """Class that will define how DC motors will behave"""
    def __init__(self, in_pin1: int, in_pin2: int, pwm_pin:int ):
        super().__init__(in_pin1, in_pin2, pwm_pin)
        self.pwm_pin = pwm_pin
        self.IN1 = in_pin1
        self.IN2 = in_pin2

        self.pwm = GPIO.PWM(self.pwm_pin, 50)
        self.pwm.start(0)

    def move_forward(self, speed: int):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def move_back(self, speed: int):
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

class Solenoid(Motor):
    def __init__(self, out_pin: int):
        super().__init__(out_pin)
        self.control_pin = out_pin

    def open(self):
        GPIO.output(self.control_pin, GPIO.HIGH)

    def close(self):
        GPIO.output(self.control_pin, GPIO.LOW)


