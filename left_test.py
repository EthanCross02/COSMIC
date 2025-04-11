import MotorClass
import RPi.GPIO as GPIO

LEFT_STEP = MotorClass.Stepper(38, 40)
LEFT_FLANGE = MotorClass.SmallServo(32)
LEFT_ELEVATOR = MotorClass.ServoMotor(26)

# Left Node Magazine
LEFT_TRAY = MotorClass.DCMotor(35, 37)

def wait():
    cont = input('Continue? (y/n): ').lower().strip() == 'y'
    if cont:
        return
    else:
        quit()

def main():
    try:
        speed = int(input('Speed: '))
        time = int(input('Time: '))
        LEFT_TRAY.move_motor(speed, time)
        wait()
        pos = int(input('Position: '))
        LEFT_ELEVATOR.change_pos(pos)
        wait()
        LEFT_FLANGE.open_close()
        wait()
        pos = int(input('Position: '))
        LEFT_ELEVATOR.change_pos(pos)
        wait()
        speed = int(input('Speed: '))
        time = int(input('Time: '))
        LEFT_TRAY.move_motor(speed, time)
        wait()
        pos = int(input('Position: '))
        LEFT_ELEVATOR.change_pos(pos)

    finally:
        GPIO.cleanup()
        print("Pins are cleaned")

if __name__ == '__main__':
    main()