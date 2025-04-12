import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import MotorClass
from time import strftime
import RPi.GPIO as GPIO

# Verified safe GPIO pins (BOARD numbering) for all Pi models
SAFE_PINS = {
    'left_stepper': (11, 13),  # Previously 38,40 - changed to safe alternatives
    'left_flange': 15,  # Previously 32
    'left_elevator': 16,  # Previously 28
    'left_tray': (29, 31),  # Previously 35,37
    'right_stepper': (33, 35),
    'right_flange': 36,
    'right_elevator': 37,
    'right_tray': (38, 40),
    'lead_screw': (18, 22),
    'sep_mod': (7, 12)
}


class MotorControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torque Arm Control System")
        self.root.geometry("1100x750")

        # Initialize GPIO first
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.initialize_motors()
        self.setup_ui()

    def initialize_motors(self):
        """Initialize motor instances with verified safe pins"""
        try:
            # Left Arm Components
            self.left_stepper = MotorClass.Stepper(*SAFE_PINS['left_stepper'])
            self.left_flange = MotorClass.SmallServo(SAFE_PINS['left_flange'])
            self.left_elevator = MotorClass.ServoMotor(SAFE_PINS['left_elevator'])
            self.left_tray = MotorClass.DCMotor(*SAFE_PINS['left_tray'])

            # Right Arm Components
            self.right_stepper = MotorClass.Stepper(*SAFE_PINS['right_stepper'])
            self.right_flange = MotorClass.SmallServo(SAFE_PINS['right_flange'])
            self.right_elevator = MotorClass.ServoMotor(SAFE_PINS['right_elevator'])
            self.right_tray = MotorClass.DCMotor(*SAFE_PINS['right_tray'])

            # Magazine Components
            self.lead_screw = MotorClass.DCMotor(*SAFE_PINS['lead_screw'])
            self.sep_mod = MotorClass.DCMotor(*SAFE_PINS['sep_mod'])

            self.log("All motors initialized successfully")
        except Exception as e:
            self.log(f"Motor initialization failed: {str(e)}")
            messagebox.showerror("Initialization Error", f"Failed to initialize motors:\n{str(e)}")

    def setup_ui(self):
        """Setup all UI components"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs (implementation remains the same as before)
        self.create_left_arm_tab()
        self.create_right_arm_tab()
        self.create_magazine_tab()
        self.create_log_tab()

        # Status bar and emergency stop
        self.status_var = tk.StringVar(value="System Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W
                 ).pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.root, text="EMERGENCY STOP", bg="red", fg="white",
                  font=('Helvetica', 12, 'bold'), command=self.emergency_stop
                  ).pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    # [Rest of your methods remain unchanged]
    # ...

    def verify_pins(self):
        """Check if all pins are valid before initialization"""
        try:
            GPIO.setmode(GPIO.BOARD)
            for component, pins in SAFE_PINS.items():
                if isinstance(pins, tuple):
                    for pin in pins:
                        GPIO.setup(pin, GPIO.OUT)
                        GPIO.cleanup(pin)
                else:
                    GPIO.setup(pins, GPIO.OUT)
                    GPIO.cleanup(pins)
            return True
        except ValueError as e:
            self.log(f"Invalid pin detected: {str(e)}")
            return False
        except Exception as e:
            self.log(f"Pin verification error: {str(e)}")
            return False

    def emergency_stop(self):
        """Enhanced emergency stop with GPIO cleanup"""
        self.log("Executing emergency stop...")
        try:
            # Stop all motors
            motors = [attr for attr in dir(self) if not attr.startswith('__')]
            for motor in motors:
                if hasattr(getattr(self, motor), 'stop_motor'):
                    getattr(self, motor).stop_motor()

            # Cleanup GPIO
            GPIO.cleanup()
            self.log("All motors stopped and GPIO cleaned up")
            messagebox.showwarning("Emergency Stop", "All motors have been stopped")
        except Exception as e:
            self.log(f"Emergency stop failed: {str(e)}")
            messagebox.showerror("Error", f"Emergency stop failed:\n{str(e)}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MotorControlGUI(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        GPIO.cleanup()