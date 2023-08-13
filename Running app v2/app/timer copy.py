import tkinter as tk

def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def start_timer():
    global elapsed_time, is_running
    is_running = True
    timer_tick()

def stop_timer():
    global is_running
    is_running = False

def reset_timer():
    global elapsed_time, is_running
    if not is_running:
        elapsed_time = 0
        is_running = False
        timer_label.config(text=format_time(elapsed_time))

def timer_tick():
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        timer_label.config(text=format_time(elapsed_time))
    timer_label.after(10, timer_tick)

elapsed_time = 0
is_running = False

root = tk.Tk()
root.title("Timer App")

# Create the outer frame
outer_frame = tk.Frame(root, bd=2)
outer_frame.pack(padx=10, pady=10)

# Create the inner frame to hold the timer
timer_frame = tk.Frame(outer_frame, bd=2)
timer_frame.pack()

# Create a canvas to place the timer label
canvas = tk.Canvas(timer_frame, width=280, height=80)
canvas.pack()

timer_label = tk.Label(canvas, text="00:00:00:000", font=("Arial", 20))
timer_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

start_button = tk.Button(outer_frame, text="Start", width=10, command=start_timer)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(outer_frame, text="Stop", width=10, command=stop_timer)
stop_button.pack(side=tk.LEFT)

reset_button = tk.Button(outer_frame, text="Reset", width=10, command=reset_timer)
reset_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
