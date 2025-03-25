import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:
        servo = MotorClass.ServoMotor(12)

        while True:
            position: int = int(input("Please enter the position of servo: "))
            servo.change_pos(position)

    finally:
        GPIO.cleanup()
        print('\nPins are cleaned\n')
        #test

if __name__ == '__main__':
    main()