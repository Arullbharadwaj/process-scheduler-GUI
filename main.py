import tkinter as tk
from gui import SchedulerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.geometry("900x700")
    root.mainloop()
