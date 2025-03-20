import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:
        servo = MotorClass.ServoMotor(40)
        servo.change_pos('CENTER')
        print("Servo Should have moved")

    finally:
        GPIO.cleanup()
        print('Pins are cleaned')

if __name__ == '__main__':
    main()