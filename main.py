import RPi.GPIO as GPIO
import MotorClass
import time

# Left Torque Arm Actuators
LEFT_STEP = MotorClass.Stepper(38, 40)
LEFT_FLANGE = MotorClass.SmallServo(32)
LEFT_ELEVATOR = MotorClass.ServoMotor(28)

# Left Node Magazine
LEFT_TRAY = MotorClass.DCMotor(35, 37)

# Right Torque Arm Actuators
RIGHT_STEPPER = MotorClass.Stepper(...)
RIGHT_FLANGE = MotorClass.SmallServo(...)
RIGHT_ELEVATOR = MotorClass.ServoMotor(...)

# Right Node Magazine
RIGHT_TRAY = MotorClass.DCMotor(...)

# Beam magazine
LEAD_SCREW = MotorClass.DCMotor(...)
SEP_MOD = MotorClass.DCMotor(...)


def wait():
    cont = input('Continue? (y/n): ').lower().strip() == 'y'
    if cont:
        return
    else:
        quit()

def main():
    try:
      ...

    finally:
        # Left Torque Arm Actuators
        LEFT_STEP.clean()
        LEFT_FLANGE.clean()
        LEFT_ELEVATOR.clean()
        # Left Node Magazine
        LEFT_TRAY.clean()
        # Right Torque Arm Actuators
        RIGHT_STEPPER.clean()
        RIGHT_FLANGE.clean()
        RIGHT_ELEVATOR.clean()
        # Right Node Magazine
        RIGHT_TRAY.clean()
        # Beam magazine
        LEAD_SCREW.clean()
        SEP_MOD.clean()
        GPIO.cleanup()
        print('All motors are low\nPins are clean')

if __name__ == "__main__":
    main()
