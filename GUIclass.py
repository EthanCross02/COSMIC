import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import MotorClass
from time import strftime


class MotorControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torque Arm Control System")
        self.root.geometry("1100x750")

        # Initialize motor instances
        self.initialize_motors()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_left_arm_tab()
        self.create_right_arm_tab()
        self.create_magazine_tab()
        self.create_log_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Emergency stop button
        estop_btn = tk.Button(root, text="EMERGENCY STOP", bg="red", fg="white",
                              font=('Helvetica', 12, 'bold'), command=self.emergency_stop)
        estop_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def initialize_motors(self):
        """Initialize all motor instances using MotorClass"""
        # Left Torque Arm
        self.left_stepper = MotorClass.Stepper(38, 40)
        self.left_flange = MotorClass.SmallServo(32)
        self.left_elevator = MotorClass.ServoMotor(28)

        # Left Node Magazine
        self.left_tray = MotorClass.DCMotor(35, 37)

        # Right Torque Arm
        self.right_stepper = MotorClass.Stepper(36, 38)  # Example pins
        self.right_flange = MotorClass.SmallServo(33)  # Example pins
        self.right_elevator = MotorClass.ServoMotor(29)  # Example pins

        # Right Node Magazine
        self.right_tray = MotorClass.DCMotor(31, 32)  # Example pins

        # Beam Magazine
        self.lead_screw = MotorClass.DCMotor(22, 23)  # Magazine raiser
        self.sep_mod = MotorClass.DCMotor(24, 25)  # Peg separator

    def create_left_arm_tab(self):
        """Tab for left torque arm controls with positional elevator"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Left Torque Arm")

        # Stepper Motor Control
        stepper_frame = ttk.LabelFrame(tab, text="Stepper Motor", padding=10)
        stepper_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(stepper_frame, text="Steps:").grid(row=0, column=0)
        self.left_step_entry = ttk.Entry(stepper_frame)
        self.left_step_entry.grid(row=0, column=1)

        ttk.Label(stepper_frame, text="Speed (ms delay):").grid(row=1, column=0)
        self.left_speed_entry = ttk.Entry(stepper_frame)
        self.left_speed_entry.insert(0, "0.003")
        self.left_speed_entry.grid(row=1, column=1)

        move_btn = ttk.Button(stepper_frame, text="Move", command=self.move_left_stepper)
        move_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Flange Control
        flange_frame = ttk.LabelFrame(tab, text="Flange Position Control", padding=10)
        flange_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(flange_frame, text="Position (0-100):").grid(row=0, column=0)
        self.left_flange_pos = ttk.Entry(flange_frame)
        self.left_flange_pos.grid(row=0, column=1)

        set_btn = ttk.Button(flange_frame, text="Set Position", command=self.set_left_flange_pos)
        set_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # Elevator Control (Positional Input)
        elevator_frame = ttk.LabelFrame(tab, text="Elevator Position Control", padding=10)
        elevator_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Label(elevator_frame, text="Position (0-100):").pack(pady=(10, 5))
        self.left_elevator_pos = ttk.Entry(elevator_frame)
        self.left_elevator_pos.pack(pady=5)

        set_btn = ttk.Button(elevator_frame, text="Set Elevator Position",
                             command=self.set_left_elevator_pos)
        set_btn.pack(pady=10)

        # Configure tab grid
        for i in range(2):
            tab.grid_rowconfigure(i, weight=1)
            tab.grid_columnconfigure(i, weight=1)

    def create_right_arm_tab(self):
        """Tab for right torque arm controls with positional elevator"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Right Torque Arm")

        # Stepper Motor Control
        stepper_frame = ttk.LabelFrame(tab, text="Stepper Motor", padding=10)
        stepper_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(stepper_frame, text="Steps:").grid(row=0, column=0)
        self.right_step_entry = ttk.Entry(stepper_frame)
        self.right_step_entry.grid(row=0, column=1)

        ttk.Label(stepper_frame, text="Speed (ms delay):").grid(row=1, column=0)
        self.right_speed_entry = ttk.Entry(stepper_frame)
        self.right_speed_entry.insert(0, "0.003")
        self.right_speed_entry.grid(row=1, column=1)

        move_btn = ttk.Button(stepper_frame, text="Move", command=self.move_right_stepper)
        move_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Flange Control
        flange_frame = ttk.LabelFrame(tab, text="Flange Position Control", padding=10)
        flange_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(flange_frame, text="Position (0-100):").grid(row=0, column=0)
        self.right_flange_pos = ttk.Entry(flange_frame)
        self.right_flange_pos.grid(row=0, column=1)

        set_btn = ttk.Button(flange_frame, text="Set Position", command=self.set_right_flange_pos)
        set_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # Elevator Control (Positional Input)
        elevator_frame = ttk.LabelFrame(tab, text="Elevator Position Control", padding=10)
        elevator_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Label(elevator_frame, text="Position (0-100):").pack(pady=(10, 5))
        self.right_elevator_pos = ttk.Entry(elevator_frame)
        self.right_elevator_pos.pack(pady=5)

        set_btn = ttk.Button(elevator_frame, text="Set Elevator Position",
                             command=self.set_right_elevator_pos)
        set_btn.pack(pady=10)

        # Configure tab grid
        for i in range(2):
            tab.grid_rowconfigure(i, weight=1)
            tab.grid_columnconfigure(i, weight=1)

    def create_magazine_tab(self):
        """Tab for magazine controls (unchanged from previous version)"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Magazines")

        # Left Magazine
        left_mag_frame = ttk.LabelFrame(tab, text="Left Magazine", padding=10)
        left_mag_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(left_mag_frame, text="Speed (0-100):").grid(row=0, column=0)
        self.left_mag_speed = ttk.Entry(left_mag_frame)
        self.left_mag_speed.grid(row=0, column=1)

        ttk.Label(left_mag_frame, text="Run Time (s):").grid(row=1, column=0)
        self.left_mag_time = ttk.Entry(left_mag_frame)
        self.left_mag_time.grid(row=1, column=1)

        move_btn = ttk.Button(left_mag_frame, text="Move Tray",
                              command=lambda: self.move_dc_motor(self.left_tray,
                                                                 self.left_mag_speed.get(),
                                                                 self.left_mag_time.get()))
        move_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Right Magazine
        right_mag_frame = ttk.LabelFrame(tab, text="Right Magazine", padding=10)
        right_mag_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        ttk.Label(right_mag_frame, text="Speed (0-100):").grid(row=0, column=0)
        self.right_mag_speed = ttk.Entry(right_mag_frame)
        self.right_mag_speed.grid(row=0, column=1)

        ttk.Label(right_mag_frame, text="Run Time (s):").grid(row=1, column=0)
        self.right_mag_time = ttk.Entry(right_mag_frame)
        self.right_mag_time.grid(row=1, column=1)

        move_btn = ttk.Button(right_mag_frame, text="Move Tray",
                              command=lambda: self.move_dc_motor(self.right_tray,
                                                                 self.right_mag_speed.get(),
                                                                 self.right_mag_time.get()))
        move_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Beam Magazine Controls
        beam_frame = ttk.LabelFrame(tab, text="Beam Magazine", padding=10)
        beam_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Lead Screw (Magazine Raiser)
        ttk.Label(beam_frame, text="Lead Screw (Raiser):").grid(row=0, column=0)
        self.lead_screw_speed = ttk.Entry(beam_frame)
        self.lead_screw_speed.grid(row=0, column=1)
        ttk.Label(beam_frame, text="Run Time (s):").grid(row=0, column=2)
        self.lead_screw_time = ttk.Entry(beam_frame)
        self.lead_screw_time.grid(row=0, column=3)
        move_btn = ttk.Button(beam_frame, text="Move Lead Screw",
                              command=lambda: self.move_dc_motor(self.lead_screw,
                                                                 self.lead_screw_speed.get(),
                                                                 self.lead_screw_time.get()))
        move_btn.grid(row=0, column=4, padx=5)

        # Separator Module
        ttk.Label(beam_frame, text="Separator Module:").grid(row=1, column=0)
        self.sep_mod_speed = ttk.Entry(beam_frame)
        self.sep_mod_speed.grid(row=1, column=1)
        ttk.Label(beam_frame, text="Run Time (s):").grid(row=1, column=2)
        self.sep_mod_time = ttk.Entry(beam_frame)
        self.sep_mod_time.grid(row=1, column=3)
        move_btn = ttk.Button(beam_frame, text="Move Separator",
                              command=lambda: self.move_dc_motor(self.sep_mod,
                                                                 self.sep_mod_speed.get(),
                                                                 self.sep_mod_time.get()))
        move_btn.grid(row=1, column=4, padx=5)

        # Configure grid
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

    def create_log_tab(self):
        """Tab for system logs with timestamps"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="System Log")

        self.log_text = ScrolledText(tab, wrap=tk.WORD, width=100, height=30)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        clear_btn = ttk.Button(tab, text="Clear Log", command=self.clear_log)
        clear_btn.pack(pady=5)

    # Motor control methods
    def move_left_stepper(self):
        try:
            steps = int(self.left_step_entry.get())
            delay = float(self.left_speed_entry.get())
            threading.Thread(target=self.left_stepper.move_motor, args=(steps, delay)).start()
            self.log(f"Left stepper moving {steps} steps with {delay}s delay")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def set_left_flange_pos(self):
        try:
            pos = int(self.left_flange_pos.get())
            if 0 <= pos <= 100:
                threading.Thread(target=self.left_flange.change_pos, args=(pos,)).start()
                self.log(f"Setting left flange to position {pos}")
            else:
                messagebox.showerror("Error", "Position must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid position value")

    def set_left_elevator_pos(self):
        """Set left elevator to specific position (0-100)"""
        try:
            pos = int(self.left_elevator_pos.get())
            if 0 <= pos <= 100:
                # Convert 0-100 range to servo range (adjust as needed)
                servo_pos = int((pos / 100) * 180)  # Example conversion to 0-180 degrees
                threading.Thread(target=self.left_elevator.change_pos, args=(servo_pos,)).start()
                self.log(f"Setting left elevator to position {pos}%")
            else:
                messagebox.showerror("Error", "Position must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid position value")

    def move_right_stepper(self):
        try:
            steps = int(self.right_step_entry.get())
            delay = float(self.right_speed_entry.get())
            threading.Thread(target=self.right_stepper.move_motor, args=(steps, delay)).start()
            self.log(f"Right stepper moving {steps} steps with {delay}s delay")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def set_right_flange_pos(self):
        try:
            pos = int(self.right_flange_pos.get())
            if 0 <= pos <= 100:
                threading.Thread(target=self.right_flange.change_pos, args=(pos,)).start()
                self.log(f"Setting right flange to position {pos}")
            else:
                messagebox.showerror("Error", "Position must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid position value")

    def set_right_elevator_pos(self):
        """Set right elevator to specific position (0-100)"""
        try:
            pos = int(self.right_elevator_pos.get())
            if 0 <= pos <= 100:
                # Convert 0-100 range to servo range (adjust as needed)
                servo_pos = int((pos / 100) * 180)  # Example conversion to 0-180 degrees
                threading.Thread(target=self.right_elevator.change_pos, args=(servo_pos,)).start()
                self.log(f"Setting right elevator to position {pos}%")
            else:
                messagebox.showerror("Error", "Position must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid position value")

    def move_dc_motor(self, motor, speed_str, time_str):
        try:
            speed = int(speed_str)
            run_time = float(time_str)
            threading.Thread(target=motor.move_motor, args=(speed, run_time)).start()
            self.log(f"Moving {motor.__class__.__name__} at {speed}% for {run_time} seconds")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def emergency_stop(self):
        """Emergency stop all motors"""
        self.log("EMERGENCY STOP ACTIVATED!")
        messagebox.showwarning("Emergency", "All motors stopped")
        # Add actual emergency stop logic here

    def log(self, message):
        """Add timestamped message to log"""
        timestamp = strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.status_var.set(message)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Log cleared")

    def on_closing(self):
        """Cleanup on window close"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Cleanup all motors
            motors = [
                self.left_stepper, self.left_flange, self.left_elevator, self.left_tray,
                self.right_stepper, self.right_flange, self.right_elevator, self.right_tray,
                self.lead_screw, self.sep_mod
            ]
            for motor in motors:
                try:
                    if hasattr(motor, 'stop_motor'):
                        motor.stop_motor()
                    if hasattr(motor, 'clean'):
                        motor.clean()
                except Exception as e:
                    self.log(f"Error cleaning {motor.__class__.__name__}: {str(e)}")
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MotorControlGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()