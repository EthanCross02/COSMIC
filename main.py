import GUIclass as gui
import MotorClass
import time

def main():

    #initialize all motors

    left_stepper = MotorClass.Stepper(None, None)
    right_stepper = MotorClass.Stepper(None, None)

    left_sol = MotorClass.Solenoid(None)
    right_sol = MotorClass.Solenoid(None)

    # DC Motors are not correct yet
    #left_pusher = MotorClass.DCMotor(None, None)
    #right_pusher = MotorClass.DCMotor(None, None)

    left_servo = MotorClass.ServoMotor(None)
    right_servo = MotorClass.ServoMotor(None)

    mag_servo = MotorClass.ServoMotor(None)
    #mag_screw = MotorClass.DCMotor(None, None)


    
if __name__ == "__main__":
    main()
