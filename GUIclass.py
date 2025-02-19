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

    def frame_input(self, frame1, frame2):
        """
        This method adds the button frames created in main.py.
        This could be built dynamically, but for now hard-code is fine
        """
        frame1.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        frame2.grid(row=0, column=2, sticky=tk.W + tk.E, padx=5, pady=5)

    def start(self):
        """This method allows the starting of the GUI whenever construction is complete"""
        self.mainloop()


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


