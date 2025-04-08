import MotorClass
import time
import RPi.GPIO as GPIO

def small(servo):
    while True:
        Open_close = input('Open or Close? (o/c): ').lower().strip() == 'o'
        if Open_close == True:
            servo.change_pos(25)
            print('Open')
        else:
            servo.change_pos(15)
            print("Closed")

def big(servo):
    while True:
        position = input('Enter Position: ')
        servo.change_pos(position)

def main():
    try:
        small_sel = input('Small? (y/n): ').lower().strip() == 'y'
        if small_sel == True:
            servo = MotorClass.SmallServo(12)
            small(servo)
        else:
            servo = MotorClass.ServoMotor(12)
            big(servo)


    finally:
        GPIO.cleanup()
        print('\nPins are cleaned\n')
        #test

if __name__ == '__main__':
    main()