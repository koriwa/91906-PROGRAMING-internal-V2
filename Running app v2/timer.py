from tkinter import *
from tkinter import ttk
import datetime
import customtkinter
import tkinter as tk
from PIL import ImageTk, Image
import threading
import sys
import time
import subprocess
import psutil

# Create the main root window
root = Tk()
root.geometry("495x595")
root.title("Timer")
root.resizable(width=False, height=False)

# Initialize the username variable with a default value "Guest"
logged_in_username = ""

# Check if a username is provided as a command-line argument, if not, set it as "Guest"
if (len(sys.argv) > 1):
    logged_in_username = sys.argv[1]

if (logged_in_username == ""):
    logged_in_username = "Guest"

# Print the logged-in username for debugging purposes
print(logged_in_username)

# Define the file name for storing user timer data
user_timer_data_file = "db/user_timer_data.txt"

# Get battery percentage using psutil
#battery = psutil.sensors_battery()
#percent = battery.percent

# Function to center a window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(root)


# Formats the time 
def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"


# Function to start the timer
def start_timer():
    global elapsed_time, is_running
    is_running = True
    timer_tick()


# Function to stop the timer
def stop_timer():
    global is_running
    is_running = False


# Function to reset the timer
def reset_timer():
    global elapsed_time, is_running
    if not is_running:
        elapsed_time = 0
        is_running = False
        timer_label.config(text=format_time(elapsed_time))


# Handles each tick of the timer
def timer_tick():
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        timer_label.config(text=format_time(elapsed_time))
    timer_label.after(10, timer_tick)


# Function to get the suffix for a day number (e.g., 1st, 2nd, 3rd, 4th, ...)
def get_day_suffix(day):
    if (10 <= day <= 20):
        return "th"
    else:
        suffixes = {
            1: "st",
            2: "nd",
            3: "rd"
        }
        suffix = suffixes.get(day % 10, "th")
        return suffix


# Function to validate allowed inputs (digits, empty input, or a single decimal number)
def allowed_inputs(input_text):
    if input_text.isdigit():  # Check if the input consists only of digits
        return True
    elif input_text == "":  # Allow an empty input
        return True
    elif input_text.count('.') == 1 and input_text.replace('.', '').isdigit():
        return True
    else:
        return False

current_date = datetime.date.today()

day = current_date.day
month = current_date.strftime("%B")
year = current_date.year

ordinal_suffix = get_day_suffix(day)
formatted_date = f"{month} {day}{ordinal_suffix}, {year}"

date_to_display = StringVar()
date_to_display.set(formatted_date)

background = r"assets\timer_backgroundv9.png"
background_image = ImageTk.PhotoImage(Image.open(background))

background_label = ttk.Label(root, image=background_image)
background_label.place(x=-2, y=-2)

date_label = ttk.Label(root, textvariable=date_to_display,
                       font=("Arial", 15, "bold"), background="white")
date_label.place(relx=0.5, y=67, anchor=tk.CENTER)

elapsed_time = 0
is_running = False

selected_measurement = StringVar()
selected_measurement.set("kilometer")

# Function to change the measurement type (kilometer/meter) for distance
def change_measurement_type(button_type):
    if (selected_measurement.get() == "kilometer" and button_type == "meter_button"):
        selected_measurement.set("meter")
        # Configure the meter_button appearance
        meter_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        kilometer_button.configure(fg_color="lightgray", hover_color="gray")
        distance_label_text.set("SET DISTANCE (CURRENT: METERS)")
        # Place the meter_button
        root.after(0, lambda: meter_button.place(relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(relx=0.65, y=225, anchor=tk.CENTER))

    elif (selected_measurement.get() == "meter" and button_type == "kilometer_button"):
        selected_measurement.set("kilometer")
        # Configure the kilometer_button appearance
        kilometer_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        meter_button.configure(fg_color="lightgray", hover_color="gray")
        distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")
        # Place the kilometer_button
        root.after(0, lambda: kilometer_button.place(relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER))

    elif (button_type == "kilometer_button"):
        # Place the kilometer_button
        root.after(0, lambda: kilometer_button.place(relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER))

    elif (button_type == "meter_button"):
        # Place the meter_button
        root.after(0, lambda: meter_button.place(relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(relx=0.65, y=225, anchor=tk.CENTER))


# Function to show the error message and hide it after 2000ms
def show_error():
    error_message.place(relx=0.5, y=465, anchor=tk.CENTER)
    root.after(2000, lambda: error_message.place_forget())


# Function to record the progress with the provided distance
def record_progress():
    root.after(0, lambda: save_progress_button.place(relx=0.5, y=502, anchor=tk.CENTER))
    root.after(50, lambda: save_progress_button.place(relx=0.5, y=500, anchor=tk.CENTER))

    if (ditance_entry.get() == ""):
        # If distance is not provided, show an error message in a new thread
        error_thread = threading.Thread(target=show_error)
        error_thread.start()
        return
    else:
        if not (is_running):
            distance_string = str(ditance_entry.get())
            set_distance = 0

            if selected_measurement.get() == "kilometer":
                if distance_string.endswith('.'):
                    distance_string = distance_string[:-1]
                    set_distance = float(distance_string) * 1000
                else:
                    set_distance = float(distance_string) * 1000
            elif (selected_measurement.get() == "meter"):
                if distance_string.endswith('.'):
                    distance_string = distance_string[:-1]
                    set_distance = float(distance_string)
                else:
                    set_distance = distance_string

            user_found = BooleanVar()
            user_found.set(False)

            # Open the user_timer_data_file in read and write mode
            user_timer_data = open(user_timer_data_file, "r+")
            lines = user_timer_data.readlines()

            for index, line in enumerate(lines):
                if logged_in_username.upper().strip() in line:
                    # If user found, update the corresponding line
                    user_found.set(True)
                    line_list = line.split("=")
                    new_line = "{}={}={}={}\n".format(logged_in_username.upper().strip(), str(
                        format_time(elapsed_time)), set_distance, str(int(time.time())))

                    lines[index] = new_line
                    user_timer_data.seek(0)

                    user_timer_data.writelines(lines)
                    user_timer_data.truncate()
                    return

            if not (user_found.get() == True):
                # If user not found, create a new line with user data
                line_list = line.split("=")
                user_timer_data.write("{}={}={}={}\n".format(logged_in_username.upper().strip(
                ), str(format_time(elapsed_time)), set_distance, str(int(time.time()))))
                user_timer_data.close()
                return


# Function to handle focus event on distance entry
def distance_entry_focus(event):
    ditance_entry.configure(validate="key", validatecommand=(validation, "%P"))


# Function to update the battery percentage every 1 second
#def update_battery_percentage():
    #battery = psutil.sensors_battery()
   # percent = battery.percent
   # battery_label.config(text=f"{percent}%")
    #root.after(1000, update_battery_percentage)  # Updates every 1 second

    
#battery_label = tk.Label(root, text=f"{percent}%", font=("Arial", 12))
#battery_label.place(relx=0.9, y=10)

distance_label_text = StringVar()
distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")

distance_label = ttk.Label(
    root, textvariable=distance_label_text, font=("Arial", 10, "bold"))
distance_label.place(relx=0.5, y=135, anchor=tk.CENTER)

meter_button = customtkinter.CTkButton(root, text="      METER      ", text_color="white", fg_color="lightgray",
                                       hover_color="gray", corner_radius=50, width=10, command=lambda: change_measurement_type("meter_button"))
meter_button.place(relx=0.65, y=225, anchor=tk.CENTER)

kilometer_button = customtkinter.CTkButton(root, text="KILOMETER", text_color="white", fg_color="#f99009",
                                           hover_color="#f97f01", corner_radius=50, width=10, command=lambda: change_measurement_type("kilometer_button"))
kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER)

validation = root.register(allowed_inputs)  # Register the validation function
ditance_entry = customtkinter.CTkEntry(root, placeholder_text="  TRAVELLED DISTANCE", bg_color="white",
                                       fg_color="white", border_color="white", text_color="black", font=("Arial", 19, "bold"), width=255)
ditance_entry.place(relx=0.5, y=166.5, anchor=tk.CENTER)
ditance_entry.bind("<FocusIn>", distance_entry_focus)

outer_frame = Frame(root)
outer_frame.place(relx=0.5, y=400, anchor=tk.CENTER)

timer_text_label = ttk.Label(
    root, text="T I M E R", font=("Arial", 15, "bold"))  
timer_text_label.place(relx=0.5, y=295, anchor=tk.CENTER)

timer_label = ttk.Label(root, text="00:00:00:000",    
                        font=("Arial", 35), background="white")
timer_label.place(relx=0.5, y=345, anchor=tk.CENTER)

start_button = ttk.Button(outer_frame, text="Start",
                          width=10, command=start_timer)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(outer_frame, text="Stop",
                         width=10, command=stop_timer)
stop_button.pack(side=tk.LEFT)

reset_button = ttk.Button(outer_frame, text="Reset",
                          width=10, command=reset_timer)
reset_button.pack(side=tk.LEFT, padx=10)

error_message = ttk.Label(root, text="A DISTANCE MUST BE SET TO RECORD THE PROGRESS!", font=(
    "Arial", 11, "bold"), foreground="red")
save_progress_button = customtkinter.CTkButton(root, text="RECORD PROGRESS", text_color="white", fg_color="#f98a06",
                                               hover_color="#f9ac06", corner_radius=50, width=10, command=record_progress, font=("Arial", 20, "bold"))
save_progress_button.place(relx=0.5, y=500, anchor=tk.CENTER)

#update_battery_percentage()

root.mainloop()
