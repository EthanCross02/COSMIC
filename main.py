import GUIclass as gui

def makeGUI():
    # Create the GUI instance
    controller = gui.GUI("Motor Controller")

    #Create CustomFrame object for button frames
    left_button = gui.CustomFrame(controller, "Servo Left", "Pusher Left", "Solenoid Left", "Stepper Left")
    right_button = gui.CustomFrame(controller, "Servo Right", "Pusher Right", "Solenoid Right", "Stepper Right")
    mag_button = gui.MagFrame(controller, "Servo", "Magazine")

    # Add frames to the GUI
    controller.frame_input(left_button, right_button, mag_button)

    return controller


def main():

    # Start the GUI
    controller = makeGUI()
    controller.start()

if __name__ == "__main__":
    main()
