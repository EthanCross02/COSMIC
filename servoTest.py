import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:
        small = input('Small? (y/n): ').lower().strip() == 'y'
        if small == True:
            servo = MotorClass.SmallServo(12)
        else:
            servo = MotorClass.ServoMotor(13)
        while True:
            position: int = int(input("Please enter the position of servo: "))
            servo.change_pos(position)

    finally:
        GPIO.cleanup()
        print('\nPins are cleaned\n')
        #test

if __name__ == '__main__':
    main()