import MotorClass
import RPi.GPIO as GPIO
import time

def main():
    try:

        motor = MotorClass.DCMotor(38, 40)
        print('Motor is moving backwards')
        motor.move_motor(-20, 5.0)
        print('Motor is moving forwards')
        motor.move_motor(80, 5.0)
        print('Motor is stopped')
        '''
        pin1 = 38
        pin2 = 40
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        in1 = GPIO.PWM(pin1, 50)
        in2 = GPIO.PWM(pin2, 50)
        in1.start(0)
        in2.start(0)

        in1.ChangeDutyCycle(30)
        print('Motor is moving\n')
        time.sleep(5)
        print("Motor has stopped\n")
        '''
    finally:
        GPIO.cleanup()
        print("Pins are clean\n")

if __name__ == '__main__':
    main()
