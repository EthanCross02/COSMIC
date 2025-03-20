import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:
        '''
        servo = MotorClass.ServoMotor(40)
        servo.change_pos('CENTER')
        print("Servo Should have moved")
        '''

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)
        servo = GPIO.PWM(40, 250)
        servo.ChangeDutyCycle(30)
        print("Servo Should have moved")
        time.sleep(5)
        servo.ChangeDutyCycle(0)
        print("Servo Should have moved")
        time.sleep(5)
        servo.ChangeDutyCycle(60)
        print("Servo Should have moved")
    finally:
        GPIO.cleanup()
        print('Pins are cleaned')

if __name__ == '__main__':
    main()