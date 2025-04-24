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

import RPi.GPIO as GPIO
from typing import Final
import time

NEUTRAL: Final[int] = 0 #this is an assumption on servo neutral position

SERVO_FREQ: Final[int] = 200
SERVO_MIN: Final[float] = 500      #in microseconds
SERVO_MAX: Final[float] = 2.5e3      #in microseconds

SMALL_MIN: Final[float] = 1e-3       #in seconds
SMALL_MAX: Final[float] = 4e-3          # seconds
SMALL_FREQ: Final[int] = SERVO_FREQ        # Hz


GPIO.setmode(GPIO.BOARD)


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

    def clean(self):
        GPIO.output(self.output1, GPIO.LOW)
        if self.output2 is not None:
            GPIO.output(self.output2, GPIO.LOW)
        if self.output3 is not None:
            GPIO.output(self.output3, GPIO.LOW)



class ServoMotor(Motor):
    def __init__(self, pwm_pin: int):
        super().__init__(pwm_pin)
        self.pwm_pin = pwm_pin
        self.pwm = GPIO.PWM(self.pwm_pin, SERVO_FREQ)
        self.pwm.start(100)


    def change_pos(self, position: int):
        """Method to change the position of as servo"""
        current_pos = self.position
        new_pos = position
        difference = new_pos - current_pos
        if difference < 0:
            for i in range(abs(difference)):
                self.step_up(current_pos-i)
                time.sleep(0.1)
                self.position = current_pos-i
        if difference > 0:
            for i in range(abs(difference)):
                self.step_up(current_pos+i)
                time.sleep(0.1)
                self.position = current_pos+i

    def step_up(self, position: int):
        """Method to change the position of as servo"""
        #state = servo_setting(position)
        Pulse_width = ((position/100)*2000)+500
        state = (Pulse_width*(SERVO_FREQ/1000000))*100
        #print(state)
        self.pwm.ChangeDutyCycle(state)
        time.sleep(0.1)

    def clean(self):
        self.pwm.stop()
        GPIO.cleanup(self.pwm_pin)

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
            self.pwm2.start(0)
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

    def move_motor(self, steps: int, delay: float=0.003):
        """
        This method will take an input for steps as a positive or negative number
        and move the stepper in the direction indicated by the sign. The delay is also the speed
        of the motor and is set by default if no other variable is passed. This will also keep track of the
        position
        """
        GPIO.output(self.step_pin, GPIO.HIGH)
        if steps < 0:
            GPIO.output(self.dir_pin, GPIO.HIGH)    #change this to low if you want to swap direction convention
            self.position += steps
            print("Direction is HIGH\n")
            steps=steps*-1  #allows direction to be read directly from step numbering
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)
            print("Direction is LOW\n")
            self.position += steps
        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

        print(f"New position: {self.position}")

class SmallServo(ServoMotor):

    def __init__(self, pwm_pin: int):
        super().__init__(pwm_pin)
        self.pwm_pin = pwm_pin
        self.position = 15
        self.change_pos(15)

    def open_close(self):
        if self.position == 10:
            self.change_pos(20)
            self.position = 20
        if self.position == 20:
            self.change_pos(10)
            self.position = 10

    def change_pos(self, position: int):
        """Method to change the position of as servo"""
        current_pos = self.position
        new_pos = position
        difference = new_pos - current_pos
        if difference < 0:
            for i in range(abs(difference)):
                self.step_up(current_pos-i)
                time.sleep(0.3)
                self.position = current_pos-i
        if difference > 0:
            for i in range(abs(difference)):
                self.step_up(current_pos+i)
                time.sleep(0.3)
                self.position = current_pos+i

    def step_up(self, position):
        # state = servo_setting(position)
        Pulse_width = SMALL_MIN + (position / 100) * (SMALL_MAX - SMALL_MIN)
        state = Pulse_width * SMALL_FREQ * 100
        # print(state)
        self.pwm.ChangeDutyCycle(state)
        time.sleep(0.1)
    def clean(self):
        self.pwm.stop()
        GPIO.cleanup(self.pwm_pin)
