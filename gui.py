import tkinter as tk
from tkinter import ttk

class ProcessSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduler")
        self.root.geometry("600x400")

        # Title
        title_label = tk.Label(root, text="CPU Process Scheduler", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Process Table
        self.tree = ttk.Treeview(root, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.pack(pady=10, fill="x")

        # Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="PID:").grid(row=0, column=0, padx=5, pady=5)
        self.pid_entry = tk.Entry(input_frame)
        self.pid_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Arrival Time:").grid(row=1, column=0, padx=5, pady=5)
        self.arrival_entry = tk.Entry(input_frame)
        self.arrival_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Burst Time:").grid(row=2, column=0, padx=5, pady=5)
        self.burst_entry = tk.Entry(input_frame)
        self.burst_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
        self.priority_entry = tk.Entry(input_frame)
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Process", command=self.add_process)
        add_button.grid(row=0, column=0, padx=10)

        schedule_button = tk.Button(button_frame, text="Run Scheduler", command=self.run_scheduler)
        schedule_button.grid(row=0, column=1, padx=10)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_table)
        clear_button.grid(row=0, column=2, padx=10)

    def add_process(self):
        pid = self.pid_entry.get()
        arrival = self.arrival_entry.get()
        burst = self.burst_entry.get()
        priority = self.priority_entry.get()
        self.tree.insert("", "end", values=(pid, arrival, burst, priority))
        self.clear_entries()

    def clear_entries(self):
        self.pid_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def run_scheduler(self):
        # Placeholder for scheduling logic
        print("Scheduler logic will run here...")

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessSchedulerGUI(root)
    root.mainloop()
