import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:
        while True:
            servo = MotorClass.ServoMotor(40)
            position: int = int(input("Please enter the position of servo: "))
            servo.change_pos(position)

    finally:
        GPIO.cleanup()
        print('\nPins are cleaned\n')

if __name__ == '__main__':
    main()