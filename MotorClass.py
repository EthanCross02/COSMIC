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
    def __init__(self, in_pin1: int, in_pin2: int):
        super().__init__(in_pin1, in_pin2)
        self.IN1 = in_pin1
        self.IN2 = in_pin2

        self.pwm1 = GPIO.PWM(self.IN1, 50)   #check to see if frequency is correct
        self.pwm2 = GPIO.PWM(self.IN2, 50)  # check to see if frequency is correct




    def move_motor(self, speed: int, run_time: float):
        if speed < 0:
            speed = speed*-1
            self.pwm1.start(0)
            self.pwm2.start(speed)
            time.sleep(run_time)
            self.stop_motor()

        else:
            self.pwm2.start()
            self.pwm1.start(speed)
            time.sleep(run_time)
            self.stop_motor()

    def stop_motor(self):
        self.pwm1.stop()
        self.pwm2.stop()

class Solenoid(Motor):
    def __init__(self, out_pin: int):
        super().__init__(out_pin)
        self.control_pin = out_pin

    def open(self):
        GPIO.output(self.control_pin, GPIO.HIGH)

    def close(self):
        GPIO.output(self.control_pin, GPIO.LOW)

class Stepper(Motor):
    """Class to define stepper motors and initialize through motors"""
    def __init__(self, step_pin: int, dir_pin: int):
        super().__init__(step_pin, dir_pin)
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.position = 0

    def move_motor(self, steps: int, delay: float=0.001):
        """
        This method will take an input for steps as a positive or negative number
        and move the stepper in the direction indicated by the sign. The delay is also the speed
        of the motor and is set by default if no other variable is passed. This will also keep track of the
        position
        """

        if steps < 0:
            GPIO.output(self.dir_pin, GPIO.HIGH)    #change this to low if you want to swap direction convention
            self.position += steps
            steps=steps*-1  #allows direction to be read directly from step numbering
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)
            self.position += steps
        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

        print(f"New position: {self.position}")





