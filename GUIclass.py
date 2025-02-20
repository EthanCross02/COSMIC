"""
This file contains each class as it is needed for the construction of the GUI

Motor control functions will be added into the class as they are made from the
MotorFunctions module. Reference the MotorFunctions module as needed for further definitions
and clarification
"""

import tkinter as tk

class GUI(tk.Tk):
    """
    This class is used to build the main widget for the GUI.
    It is a subclass of Tk as when using tkinter, each of the widgets are
    a class of themselves
    """
    def __init__(self, title):
        super().__init__()  #call the parent constructor
        """This method will initialize the GUI"""

        #Configure the main window (self)
        self.geometry("1200x800")
        self.title(title)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=3)

        # Bind close event to cleanup method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def frame_input(self, frame1, frame2, frame3):
        """
        This method adds the button frames created in main.py.
        This could be built dynamically, but for now hard-code is fine
        """
        frame1.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        frame2.grid(row=0, column=2, sticky=tk.W + tk.E, padx=5, pady=5)

        frame3.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)


    def start(self):
        """This method allows the starting of the GUI whenever construction is complete"""
        self.mainloop()

    def on_close(self):
        """Method executed when the GUI is closed"""
        print("Performing cleanup before closing...")
        GPIO.cleanup()
        print("Closing GUI...")

class MagFrame(tk.Frame):
    """
    This class is used to construct the frame for the magazine control
    """
    def __init__(self, master, label_servo, label_screw):
        super().__init__(master) #call parent constructor
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        #creating labels for the servo control and screw control
        self.servo_label = tk.Label(self, text=label_servo)
        self.servo_label.grid(row=0, column=0, sticky=tk.W)

        self.screw_label = tk.Label(self, text=label_screw)
        self.screw_label.grid(row=0, column=1, sticky=tk.E)

        #creating the buttons for the servo
        self.servo_button_open = tk.Button(self, text="OPEN")
        self.servo_button_open.grid(row=1, column=0, sticky=tk.E + tk.W)

        self.servo_button_neutral = tk.Button(self, text="NEUTRAL")
        self.servo_button_neutral.grid(row=2, column=0, sticky=tk.E + tk.W)

        self.servo_button_closed = tk.Button(self, text="CLOSED")
        self.servo_button_closed.grid(row=3, column=0, sticky=tk.E + tk.W)


        #creating buttons for screw

        self.screw_button_up = tk.Button(self, text="UP")
        self.screw_button_up.grid(row=1, column=1, sticky=tk.E + tk.W)

        self.screw_button_down = tk.Button(self, text="DOWN")
        self.screw_button_down.grid(row=2, column=1, sticky=tk.E + tk.W)


class CustomFrame(tk.Frame):
    """This class is used to build the widget for each button frame used in the gui.
    It is a subclass of tkinter.Frame"""
    def __init__(self, master, servo_name, pusher_name, solenoid_name, stepper_name):
        super().__init__(master) #call parent constructor
        """
        This method will initialize the CustomFrame object.
        As motor functions are created, custom methods to call the functions should
        be added for each of the button presses
        """

        #Creating the geometry for the button frames
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        #Creating each button widget with the name passed from main.py
        self.servo = tk.Button(self, text=servo_name)
        self.servo.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.pusher = tk.Button(self, text=pusher_name)
        self.pusher.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.solenoid = tk.Button(self, text=solenoid_name)
        self.solenoid.grid(row=1, column=0, sticky=tk.W + tk.E)

        self.stepper = tk.Button(self, text=stepper_name)
        self.stepper.grid(row=1, column=1, sticky=tk.W + tk.E)


