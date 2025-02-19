import GUIclass as gui

# Create the GUI instance
Controller = gui.GUI("Motor Controller")

# Create CustomFrame object for button frames
leftButton = gui.CustomFrame(Controller, "Servo Left", "Pusher Left", "Solenoid Left", "Stepper Left")
rightButton = gui.CustomFrame(Controller, "Servo Right", "Pusher Right", "Solenoid Right", "Stepper Right")

# Add frames to the GUI
Controller.frame_input(leftButton, rightButton)

# Start the GUI
Controller.start()