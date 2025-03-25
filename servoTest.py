import MotorClass
import time
import RPi.GPIO as GPIO

def main():
    try:

        servo = MotorClass.ServoMotor(40)
        servo.change_pos(1)
        print("Minimum")
        time.sleep(3)
        servo.change_pos(100)
        print("Maximum")
        time.sleep(3)
        servo.change_pos(50)
        print("Neutral")

        '''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)
        servo = GPIO.PWM(40, 100)
        servo.start(15)
        print("Servo Should have moved")
        time.sleep(5)
        servo.ChangeDutyCycle(20)
        print("Servo Should have moved")
        time.sleep(5)
        servo.ChangeDutyCycle(25)
        print("Servo Should have moved")
        time.sleep(5)
        servo.stop()
        '''
    finally:
        GPIO.cleanup()
        print('Pins are cleaned')

if __name__ == '__main__':
    main()