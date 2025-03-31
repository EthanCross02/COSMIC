"""
This is a test script to understand how the stepper motors work in RPi.GPIO
"""

import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:

        stepper = MotorClass.Stepper(38, 40)
        stepper.move_motor(800)
        time.sleep(1)
        stepper.move_motor(-800)
    finally:
        GPIO.cleanup()
        print("Pins are clean")

if __name__ == "__main__":
    main()
