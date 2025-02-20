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

GPIO.setmode(GPIO.BOARD)

class Motor:
    """
    This class defines all motors used in the project.

    It should be used as a parent class where other motors will be subclasses of 'Motor'.
    """

    def __init__(self, out_pin1, out_pin2=None):
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



