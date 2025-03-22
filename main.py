import GUIclass as gui
import MotorClass
import time

def main():

    stepper = MotorClass.Stepper(38,40)
    stepper.move_motor(-200)

    
if __name__ == "__main__":
    main()
