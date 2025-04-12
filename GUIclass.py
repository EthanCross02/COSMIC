import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import MotorClass
from time import strftime

# Safe GPIO pins (BOARD numbering) for Raspberry Pi 3/4
SAFE_PINS = [7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 35, 36, 37, 38, 40]


class MotorControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torque Arm Control System")
        self.root.geometry("1100x750")

        self.initialize_motors()
        self.setup_ui()

    def setup_ui(self):
        """Setup all UI components"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_left_arm_tab()
        self.create_right_arm_tab()
        self.create_magazine_tab()
        self.create_log_tab()

        self.status_var = tk.StringVar(value="System Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.root, text="EMERGENCY STOP", bg="red", fg="white",
                  font=('Helvetica', 12, 'bold'), command=self.emergency_stop
                  ).pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def initialize_motors(self):
        """Initialize motor instances with safe pins"""
        # Left Arm (your existing pins)
        self.left_stepper = MotorClass.Stepper(38, 40)
        self.left_flange = MotorClass.SmallServo(32)
        self.left_elevator = MotorClass.ServoMotor(28)
        self.left_tray = MotorClass.DCMotor(35, 37)

        # Right Arm (safe alternatives)
        self.right_stepper = MotorClass.Stepper(36, 38)
        self.right_flange = MotorClass.SmallServo(33)
        self.right_elevator = MotorClass.ServoMotor(29)
        self.right_tray = MotorClass.DCMotor(31, 32)

        # Beam Magazine
        self.lead_screw = MotorClass.DCMotor(22, 23)
        self.sep_mod = MotorClass.DCMotor(11, 13)

    def create_left_arm_tab(self):
        """Left torque arm controls"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Left Torque Arm")

        # Stepper Control
        stepper_frame = ttk.LabelFrame(tab, text="Stepper Motor", padding=10)
        stepper_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

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
        flange_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(flange_frame, text="Position (0-100):").grid(row=0, column=0)
        self.left_flange_pos = ttk.Entry(flange_frame)
        self.left_flange_pos.grid(row=0, column=1)

        ttk.Button(flange_frame, text="Set Position", command=self.set_left_flange_pos
                   ).grid(row=1, column=0, columnspan=2, pady=5)

        # Elevator Control
        elevator_frame = ttk.LabelFrame(tab, text="Elevator Position", padding=10)
        elevator_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Label(elevator_frame, text="Position (0-100):").pack(pady=(10, 5))
        self.left_elevator_pos = ttk.Entry(elevator_frame)
        self.left_elevator_pos.pack(pady=5)

        ttk.Button(elevator_frame, text="Set Position", command=self.set_left_elevator_pos
                   ).pack(pady=10)

        for i in range(2):
            tab.grid_rowconfigure(i, weight=1)
            tab.grid_columnconfigure(i, weight=1)

    def create_right_arm_tab(self):
        """Right torque arm controls"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Right Torque Arm")

        # [Same structure as create_left_arm_tab but for right side]
        # ...

    def create_magazine_tab(self):
        """Magazine controls"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Magazines")

        # [Your magazine controls implementation]
        # ...

    def create_log_tab(self):
        """System logging tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="System Log")

        self.log_text = ScrolledText(tab, wrap=tk.WORD, width=100, height=30)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(tab, text="Clear Log", command=self.clear_log).pack(pady=5)

    # Motor control methods
    def move_left_stepper(self):
        try:
            steps = int(self.left_step_entry.get())
            delay = float(self.left_speed_entry.get())
            threading.Thread(target=self.left_stepper.move_motor, args=(steps, delay)).start()
            self.log(f"Left stepper: {steps} steps, {delay}ms delay")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def set_left_flange_pos(self):
        try:
            pos = int(self.left_flange_pos.get())
            if 0 <= pos <= 100:
                threading.Thread(target=self.left_flange.change_pos, args=(pos,)).start()
                self.log(f"Left flange to {pos}%")
            else:
                messagebox.showerror("Error", "Position must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid position")

    def set_left_elevator_pos(self):
        try:
            pos = int(self.left_elevator_pos.get())
            if 0 <= pos <= 100:
                servo_pos = int((pos / 100) * 180)
                threading.Thread(target=self.left_elevator.change_pos, args=(servo_pos,)).start()
                self.log(f"Left elevator to {pos}%")
            else:
                messagebox.showerror("Error", "Position must be 0-100")
        except ValueError:
            messagebox.showerror("Error", "Invalid position")

    def log(self, message):
        """Add timestamped message to log"""
        timestamp = strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.status_var.set(message)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Log cleared")

    def emergency_stop(self):
        """Emergency stop all motors"""
        self.log("EMERGENCY STOP ACTIVATED!")
        messagebox.showwarning("Emergency", "All motors stopped")
        # Add actual emergency stop logic here

    def on_closing(self):
        """Cleanup on window close"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MotorControlGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()