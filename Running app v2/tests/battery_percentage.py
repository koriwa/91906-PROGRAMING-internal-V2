import tkinter as tk
import psutil

# Get the battery percentage
battery = psutil.sensors_battery()
percent = battery.percent

# Create the main window
window = tk.Tk()
window.geometry("500x400")
window.title("Battery Percentage")

# Create a label to display the battery percentage
battery_label = tk.Label(window, text=f"Battery percentage: {percent}%", font=("Arial", 12))
battery_label.pack(padx=10, pady=10)

# Function to update the battery percentage
def update_battery_percentage():
    battery = psutil.sensors_battery()
    percent = battery.percent
    battery_label.config(text=f"Battery percentage: {percent}%")
    window.after(5000, update_battery_percentage)  # Update every 5 seconds

# Start updating the battery percentage
update_battery_percentage()

# Set the window to always stay on top
window.wm_attributes("-topmost", 1)

# Position the window at the top left corner of the screen
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{window_width}x{window_height}+0+0")

# Start the main event loop
window.mainloop()
