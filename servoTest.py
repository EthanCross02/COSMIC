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
        servo = GPIO.PWM(40, 100)
        servo.ChangeDutyCycle(2.5)
        servo.start(7.5)
        print("Servo Should have moved")
        time.sleep(5)
        servo.ChangeDutyCycle(7.5)
        print("Servo Should have moved")
        time.sleep(5)
        servo.ChangeDutyCycle(12.5)
        print("Servo Should have moved")
        time.sleep(5)
        servo.stop()
    finally:
        GPIO.cleanup()
        print('Pins are cleaned')

if __name__ == '__main__':
    main()