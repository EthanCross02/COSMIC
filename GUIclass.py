import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import MotorClass
from time import strftime
import RPi.GPIO as GPIO

# Verified safe GPIO pins (BOARD numbering)
SAFE_PINS = {
    'left_stepper': (11, 13),
    'left_flange': 15,
    'left_elevator': 16,
    'left_tray': (29, 31),
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

        # Initialize UI first (so we can use log)
        self.setup_ui()

        # Then initialize GPIO and motors
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.initialize_motors()

    def setup_ui(self):
        """Initialize all UI components first"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create log tab first so we can use it
        self.create_log_tab()

        # Create other tabs
        self.create_left_arm_tab()
        self.create_right_arm_tab()
        self.create_magazine_tab()

        # Status bar
        self.status_var = tk.StringVar(value="System Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1,
                 relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

        # Emergency stop
        tk.Button(self.root, text="EMERGENCY STOP", bg="red", fg="white",
                  font=('Helvetica', 12, 'bold'), command=self.emergency_stop
                  ).pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def log(self, message):
        """Add timestamped message to log"""
        timestamp = strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.status_var.set(message)

    def create_log_tab(self):
        """Create the log tab first"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="System Log")

        self.log_text = ScrolledText(tab, wrap=tk.WORD, width=100, height=30)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Button(tab, text="Clear Log", command=self.clear_log).pack(pady=5)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Log cleared")

    def initialize_motors(self):
        """Initialize motor instances with safe pins"""
        try:
            # Left Arm
            self.left_stepper = MotorClass.Stepper(*SAFE_PINS['left_stepper'])
            self.left_flange = MotorClass.SmallServo(SAFE_PINS['left_flange'])
            self.left_elevator = MotorClass.ServoMotor(SAFE_PINS['left_elevator'])
            self.left_tray = MotorClass.DCMotor(*SAFE_PINS['left_tray'])

            # Right Arm
            self.right_stepper = MotorClass.Stepper(*SAFE_PINS['right_stepper'])
            self.right_flange = MotorClass.SmallServo(SAFE_PINS['right_flange'])
            self.right_elevator = MotorClass.ServoMotor(SAFE_PINS['right_elevator'])
            self.right_tray = MotorClass.DCMotor(*SAFE_PINS['right_tray'])

            # Magazine
            self.lead_screw = MotorClass.DCMotor(*SAFE_PINS['lead_screw'])
            self.sep_mod = MotorClass.DCMotor(*SAFE_PINS['sep_mod'])

            self.log("All motors initialized successfully")
        except Exception as e:
            self.log(f"Motor initialization failed: {str(e)}")
            messagebox.showerror("Initialization Error", f"Failed to initialize motors:\n{str(e)}")

    def create_left_arm_tab(self):
        """Create controls for left torque arm"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Left Arm")

        # Stepper Motor Control
        stepper_frame = ttk.LabelFrame(tab, text="Stepper Motor", padding=10)
        stepper_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(stepper_frame, text="Steps:").grid(row=0, column=0)
        self.left_step_entry = ttk.Entry(stepper_frame)
        self.left_step_entry.grid(row=0, column=1)

        ttk.Label(stepper_frame, text="Speed (ms):").grid(row=1, column=0)
        self.left_speed_entry = ttk.Entry(stepper_frame)
        self.left_speed_entry.insert(0, "0.003")
        self.left_speed_entry.grid(row=1, column=1)

        ttk.Button(stepper_frame, text="Move", command=self.move_left_stepper
                   ).grid(row=2, column=0, columnspan=2, pady=5)

        # Flange Control
        flange_frame = ttk.LabelFrame(tab, text="Flange Position", padding=10)
        flange_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(flange_frame, text="Position (0-100):").grid(row=0, column=0)
        self.left_flange_pos = ttk.Entry(flange_frame)
        self.left_flange_pos.grid(row=0, column=1)

        ttk.Button(flange_frame, text="Set Position", command=self.set_left_flange_pos
                   ).grid(row=1, column=0, columnspan=2, pady=5)

        # Elevator Control
        elevator_frame = ttk.LabelFrame(tab, text="Elevator Position", padding=10)
        elevator_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(elevator_frame, text="Position (0-100):").grid(row=0, column=0)
        self.left_elevator_pos = ttk.Entry(elevator_frame)
        self.left_elevator_pos.grid(row=0, column=1)

        ttk.Button(elevator_frame, text="Set Position", command=self.set_left_elevator_pos
                   ).grid(row=1, column=0, columnspan=2, pady=5)

    def create_right_arm_tab(self):
        """Create controls for right torque arm"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Right Arm")

        # Stepper Motor Control
        stepper_frame = ttk.LabelFrame(tab, text="Stepper Motor", padding=10)
        stepper_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(stepper_frame, text="Steps:").grid(row=0, column=0)
        self.right_step_entry = ttk.Entry(stepper_frame)
        self.right_step_entry.grid(row=0, column=1)

        ttk.Label(stepper_frame, text="Speed (ms):").grid(row=1, column=0)
        self.right_speed_entry = ttk.Entry(stepper_frame)
        self.right_speed_entry.insert(0, "0.003")
        self.right_speed_entry.grid(row=1, column=1)

        ttk.Button(stepper_frame, text="Move", command=self.move_right_stepper
                   ).grid(row=2, column=0, columnspan=2, pady=5)

        # Flange Control
        flange_frame = ttk.LabelFrame(tab, text="Flange Position", padding=10)
        flange_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(flange_frame, text="Position (0-100):").grid(row=0, column=0)
        self.right_flange_pos = ttk.Entry(flange_frame)
        self.right_flange_pos.grid(row=0, column=1)

        ttk.Button(flange_frame, text="Set Position", command=self.set_right_flange_pos
                   ).grid(row=1, column=0, columnspan=2, pady=5)

        # Elevator Control
        elevator_frame = ttk.LabelFrame(tab, text="Elevator Position", padding=10)
        elevator_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(elevator_frame, text="Position (0-100):").grid(row=0, column=0)
        self.right_elevator_pos = ttk.Entry(elevator_frame)
        self.right_elevator_pos.grid(row=0, column=1)

        ttk.Button(elevator_frame, text="Set Position", command=self.set_right_elevator_pos
                   ).grid(row=1, column=0, columnspan=2, pady=5)

    def create_magazine_tab(self):
        """Create controls for magazine system"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Magazine")

        # Left Magazine
        left_frame = ttk.LabelFrame(tab, text="Left Magazine", padding=10)
        left_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(left_frame, text="Speed (0-100):").grid(row=0, column=0)
        self.left_mag_speed = ttk.Entry(left_frame)
        self.left_mag_speed.grid(row=0, column=1)

        ttk.Label(left_frame, text="Duration (s):").grid(row=1, column=0)
        self.left_mag_duration = ttk.Entry(left_frame)
        self.left_mag_duration.grid(row=1, column=1)

        ttk.Button(left_frame, text="Run", command=self.run_left_magazine
                   ).grid(row=2, column=0, columnspan=2, pady=5)

        # Right Magazine
        right_frame = ttk.LabelFrame(tab, text="Right Magazine", padding=10)
        right_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(right_frame, text="Speed (0-100):").grid(row=0, column=0)
        self.right_mag_speed = ttk.Entry(right_frame)
        self.right_mag_speed.grid(row=0, column=1)

        ttk.Label(right_frame, text="Duration (s):").grid(row=1, column=0)
        self.right_mag_duration = ttk.Entry(right_frame)
        self.right_mag_duration.grid(row=1, column=1)

        ttk.Button(right_frame, text="Run", command=self.run_right_magazine
                   ).grid(row=2, column=0, columnspan=2, pady=5)

        # Beam Magazine Controls
        beam_frame = ttk.LabelFrame(tab, text="Beam Magazine", padding=10)
        beam_frame.pack(fill=tk.X, padx=5, pady=5)

        # Lead Screw Control
        ttk.Label(beam_frame, text="Lead Screw:").grid(row=0, column=0)
        self.lead_screw_speed = ttk.Entry(beam_frame)
        self.lead_screw_speed.grid(row=0, column=1)
        ttk.Label(beam_frame, text="Duration (s):").grid(row=0, column=2)
        self.lead_screw_duration = ttk.Entry(beam_frame)
        self.lead_screw_duration.grid(row=0, column=3)
        ttk.Button(beam_frame, text="Raise", command=self.raise_lead_screw
                   ).grid(row=0, column=4, padx=5)

        # Separator Module Control
        ttk.Label(beam_frame, text="Separator:").grid(row=1, column=0)
        self.separator_speed = ttk.Entry(beam_frame)
        self.separator_speed.grid(row=1, column=1)
        ttk.Label(beam_frame, text="Duration (s):").grid(row=1, column=2)
        self.separator_duration = ttk.Entry(beam_frame)
        self.separator_duration.grid(row=1, column=3)
        ttk.Button(beam_frame, text="Activate", command=self.activate_separator
                   ).grid(row=1, column=4, padx=5)

    # Control methods for right arm
    def move_right_stepper(self):
        try:
            steps = int(self.right_step_entry.get())
            delay = float(self.right_speed_entry.get())
            threading.Thread(target=self.right_stepper.move_motor, args=(steps, delay)).start()
            self.log(f"Right stepper: {steps} steps, {delay}ms delay")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def move_left_stepper(self):
        try:
            steps = int(self.left_step_entry.get())
            delay = float(self.left_speed_entry.get())
            threading.Thread(target=self.left_stepper.move_motor, args=(steps, delay)).start()
            self.log(f"Left stepper: {steps} steps, {delay}ms delay")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def set_right_flange_pos(self):
        try:
            pos = int(self.right_flange_pos.get())
            if 0 <= pos <= 100:
                threading.Thread(target=self.right_flange.change_pos, args=(pos,)).start()
                self.log(f"Right flange to {pos}%")
            else:
                messagebox.showerror("Error", "Must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def set_left_flange_pos(self):
        try:
            pos = int(self.left_flange_pos.get())
            if 0 <= pos <= 100:
                threading.Thread(target=self.left_flange.change_pos, args=(pos,)).start()
                self.log(f"Left flange to {pos}%")
            else:
                messagebox.showerror("Error", "Must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def set_right_elevator_pos(self):
        try:
            pos = int(self.right_elevator_pos.get())
            if 0 <= pos <= 100:
                servo_pos = int((pos / 100) * 180)
                threading.Thread(target=self.right_elevator.change_pos, args=(servo_pos,)).start()
                self.log(f"Right elevator to {pos}%")
            else:
                messagebox.showerror("Error", "Must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def set_left_elevator_pos(self):
        try:
            pos = int(self.left_elevator_pos.get())
            if 0 <= pos <= 100:
                servo_pos = int((pos / 100) * 180)
                threading.Thread(target=self.left_elevator.change_pos, args=(servo_pos,)).start()
                self.log(f"Left elevator to {pos}%")
            else:
                messagebox.showerror("Error", "Must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")
    # Magazine control methods
    def run_left_magazine(self):
        try:
            speed = int(self.left_mag_speed.get())
            duration = float(self.left_mag_duration.get())
            threading.Thread(target=self.left_tray.move_motor, args=(speed, duration)).start()
            self.log(f"Left magazine running at {speed}% for {duration}s")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def run_right_magazine(self):
        try:
            speed = int(self.right_mag_speed.get())
            duration = float(self.right_mag_duration.get())
            threading.Thread(target=self.right_tray.move_motor, args=(speed, duration)).start()
            self.log(f"Right magazine running at {speed}% for {duration}s")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def raise_lead_screw(self):
        try:
            speed = int(self.lead_screw_speed.get())
            duration = float(self.lead_screw_duration.get())
            threading.Thread(target=self.lead_screw.move_motor, args=(speed, duration)).start()
            self.log(f"Lead screw raising at {speed}% for {duration}s")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def activate_separator(self):
        try:
            speed = int(self.separator_speed.get())
            duration = float(self.separator_duration.get())
            threading.Thread(target=self.sep_mod.move_motor, args=(speed, duration)).start()
            self.log(f"Separator active at {speed}% for {duration}s")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def emergency_stop(self):
        """Emergency stop all motors"""
        self.log("Executing emergency stop...")
        try:
            motors = [attr for attr in dir(self) if not attr.startswith('__')]
            for motor in motors:
                if hasattr(getattr(self, motor), 'stop_motor'):
                    getattr(self, motor).stop_motor()
            GPIO.cleanup()
            self.log("Emergency stop complete")
        except Exception as e:
            self.log(f"Emergency stop error: {str(e)}")

    def on_closing(self):
        """Cleanup on window close"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.emergency_stop()
            self.root.destroy()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MotorControlGUI(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        GPIO.cleanup()