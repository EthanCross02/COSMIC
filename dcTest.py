import MotorClass
import RPi.GPIO as GPIO
import time

def main():
    try:
        motor = MotorClass.DCMotor(38, 40)
        motor.move_motor(-20, 5.0)


    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()