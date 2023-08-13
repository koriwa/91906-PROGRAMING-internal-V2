import tkinter
import customtkinter
import subprocess
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

# destroy current window exiting the loop so it creates a new one
window = customtkinter.CTk()
window.geometry("495x595")
window.title('Welcome')


def button_function():
    # destroy current window exiting the loop so it creates a new one
    window.destroy()
    subprocess.Popen(["python", r"log_in_page.py"])

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")
    
center_window(window)

button = customtkinter.CTkButton(
    master=window, width=220, text="home page", command=button_function, corner_radius=6)
button.place(x=100, y=220)

window.mainloop()
