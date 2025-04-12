"""
This is a test script to understand how the stepper motors work in RPi.GPIO
"""

import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:

        stepper = MotorClass.Stepper(11, 13)
        isSure = True
        while isSure == True:
            steps = int(input("Enter Steps: "))
            delay = float(input("Enter Delay: "))
            stepper.move_motor(steps, delay)
            isSure = input('Again? (y/n): ').lower().strip() == 'y'
    finally:
        GPIO.cleanup()
        print("Pins are clean\n")

if __name__ == "__main__":
    main()
