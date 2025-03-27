import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:
        motor = MotorClass.DCMotor(38,40)
        isSure = True
        while isSure == True:
            dir = input('Direction? (f/b): ').lower().strip() == 'f'
            run_time = float(input('Run time? (s): '))
            speed = float(input('Speed? (%): '))
            if dir == True:
                motor.move_motor(speed,run_time)
            else:
                motor.move_motor(-1*speed,run_time)
            isSure = input('Again? (y/n): ').lower().strip() == 'y'

    finally:
        GPIO.cleanup()
        print('\nPins are clean\nFinished\n')

if __name__ == '__main__':
    main()