import GUIclass as gui
import MotorClass
import time
def wait():
    cont = input('Continue? (y/n): ').lower().strip() == 'y'
    if cont == True:
        return
    if cont == False:


def main():

    stepper = MotorClass.Stepper(38,40)
    stepper.move_motor(-200)

    
if __name__ == "__main__":
    main()
