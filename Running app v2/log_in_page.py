import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import ImageTk, Image
import subprocess
import webbrowser
import requests

accounts_file = r"db\accounts.txt"
GOOGLE_CLIENT_ID = "1097287749447-6e9mfvfbdc3bknvh2guode8qlk4a63jh.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8000/callback"

def button_function_login(event=None):
    # grabs the username and password when they are inputted
    username = User_name_box.get()
    password = Password_box.get()

    # Check if the username and password match with the files
    with open(accounts_file, 'r+') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(':')
            if username == stored_username and password == stored_password:
                # If the things match, move on to the server authentication
                sign_in_with_google()
                return

        # If the loop completes without finding a match, display an error message
        error_label.config(text="Invalid username or password")

        # Hide the error message after 3 seconds
        sign_in_page.after(3000, lambda: error_label.config(text=""))

def button_function_signup(event=None):
    sign_in_page.destroy()
    subprocess.Popen(["python", "sign_up_page.py"])
    return

def on_enter_facebook(event):
    facebook_button.configure(
        text_color="black", hover_color="orange", fg_color="orange")

def on_leave_facebook(event):
    facebook_button.configure(
        text_color="black", hover_color="orange", fg_color='white')

def on_enter_google(event):
    google_button.configure(
        text_color="black", hover_color="orange", fg_color="orange")

def on_leave_google(event):
    google_button.configure(
        text_color="black", hover_color="orange", fg_color='white')

def sign_in_with_google():
    google_signin_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email"

    try:
        webbrowser.open(google_signin_url)

        # After opening the URL, wait for the server to handle the sign-in and get the access token
        # This is a simplified example, and in a real-world application, you should handle this better.
        # For example, use a callback function that the server can call after the sign-in process is completed.
        response = None
        while response is None:
            response = requests.get("http://localhost:8000/get_token")

        # The access token is returned by the server as text
        access_token = response.text

        # Close the sign_in_page after successful sign-in
        sign_in_page.destroy()

        # Continue to the timer.py (modify the path as needed)
        subprocess.Popen(["python", "timer.py"])

    except webbrowser.Error as e:
        print("Error opening web browser:", e)

        
sign_in_page = tk.Tk()
sign_in_page.geometry("495x595")
sign_in_page.resizable(width=False, height=False)
sign_in_page.title('Login')

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(sign_in_page)

background = r"assets\background.png"
background_image = ImageTk.PhotoImage(Image.open(background))

kat_label = tk.Label(master=sign_in_page, image=background_image)
kat_label.pack()

frame = tk.Frame(master=kat_label, width=320, height=400, bg="white")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

login_label = tk.Label(
    master=frame, text="Log into your Account", font=('Century Gothic', 20), bg="white")
login_label.place(x=20, y=45)

User_name_box = ttk.Entry(master=frame, width=40, justify="center",)
User_name_box.place(x=30, y=110)

Password_box = ttk.Entry(master=frame, width=40, justify="center", show="*")
Password_box.place(x=30, y=165)

login_button = customtkinter.CTkButton(
    master=frame, width=220, text="Login", command=button_function_login, corner_radius=100, fg_color="orange",
    hover_color="dark orange")
login_button.place(x=45, y=220)

sign_in_button = customtkinter.CTkButton(
    master=frame, width=220, text="Sign Up", command=button_function_signup, corner_radius=100, fg_color="#FFBF00",
    hover_color="dark orange")
sign_in_button.place(x=45, y=270)

google_img = r"assets\Google__G__Logo.svg.webp"
facebook_img = r"assets\facebookimg.png"

google_image = ImageTk.PhotoImage(Image.open(
    google_img).resize((20, 20), Image.LANCZOS))
facebook_image = ImageTk.PhotoImage(Image.open(
    facebook_img).resize((20, 20), Image.LANCZOS))

error_label = tk.Label(master=frame, text="", fg="red", bg="white")
error_label.place(x=30, y=260)

facebook_button = customtkinter.CTkButton(master=frame, image=facebook_image, text="Facebook", width=100,
                                          height=20, compound="left", fg_color='white', corner_radius=200, text_color='black')
facebook_button.place(x=45, y=320)

google_button = customtkinter.CTkButton(master=frame, image=google_image, text="Google", width=100,
                                        height=20, compound="left", fg_color='white', corner_radius=200, text_color='black', command=sign_in_with_google)
google_button.place(x=170, y=320)

login_button.bind("<Button-1>", button_function_login)
sign_in_button.bind("<Button-1>", button_function_signup)
facebook_button.bind("<Enter>", on_enter_facebook)
facebook_button.bind("<Leave>", on_leave_facebook)
google_button.bind("<Enter>", on_enter_google)
google_button.bind("<Leave>", on_leave_google)

sign_in_page.mainloop()
