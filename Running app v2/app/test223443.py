import tkinter as tk
from time import time, strftime, gmtime

class RunningTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Running Tracker")
        self.root.geometry("400x300")

        self.km_label = tk.Label(self.root, text="Enter the distance (km):", font=("Arial", 14))
        self.km_label.pack()

        self.km_entry = tk.Entry(self.root, font=("Arial", 14))
        self.km_entry.pack()

        self.timer_label = tk.Label(self.root, text="00:00:00:000", font=("Arial", 36))
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", width=10, command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.root, text="Stop", width=10, command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        self.start_time = None
        self.running = False

    def start_timer(self):
        if not self.running:
            self.start_time = time()
            self.update_timer()
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.km_entry.config(state=tk.DISABLED)  # Disable the entry field

    def stop_timer(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.km_entry.config(state=tk.NORMAL)  # Enable the entry field

    def update_timer(self):
        if self.running:
            elapsed_time = int((time() - self.start_time) * 1000)
            timer_str = strftime("%H:%M:%S:", gmtime(elapsed_time / 1000)) + str(elapsed_time % 1000).zfill(3)
            self.timer_label.config(text=timer_str)
        self.root.after(1, self.update_timer)

root = tk.Tk()
app = RunningTracker(root)

elapsed_time = 0
is_running = False

def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def start_timer():
    global elapsed_time, is_running
    is_running = True
    app.start_timer()
    timer_tick()

def stop_timer():
    global elapsed_time, is_running
    is_running = False
    app.stop_timer()

def timer_tick():
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        app.timer_label.config(text=format_time(elapsed_time))
    app.timer_label.after(10, timer_tick)

root.mainloop()
