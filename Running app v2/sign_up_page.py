import tkinter as tk
import customtkinter
import subprocess
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

sign_up_page = customtkinter.CTk()
sign_up_page.geometry("495x595")
sign_up_page.resizable(width=False, height=False)
sign_up_page.title('Sign Up')
accounts_file = "db/accounts.txt"

#centres the window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


center_window(sign_up_page)


def button_function():
    # Get the entered values from the input fields
    username = User_name_box.get()
    password = Password_box.get()
    confirm_password = confirm_password_box.get()

    # Reset the error label text
    error_label.config(text="")

    # Check if the username or password fields are empty
    if not username or not password:
        error_label.config(text="Please enter a valid username and password")
        sign_up_page.after(3000, lambda: error_label.config(text=""))
        return

    # Check if the password matches the confirm password
    if password == confirm_password:
        # Open the accounts file in read and write mode
        with open(accounts_file, "r+") as file:
            # Read all the lines from the file
            lines = file.readlines()

            # Check if the combination of username and password already exists in the file
            if any(username + ":" + password + "\n" in line for line in lines):
                # Print a message if the user already exists
                error_label.config(
                    text="User already exists, please create a different account")
            else:
                # If the combination doesn't exist, write the new username and password to the file and save it
                file.write(username + ":" + password + "\n")
                # Go back to the beginning of the file to update it 
                file.seek(0)
                # Read all the lines again to update the lines variable
                lines = file.readlines()

                # Print a success message
                print("Account created successfully!")

        # Destroy the sign-up page
        sign_up_page.destroy()
        # Import the log in page so the user can enter their credentials
        subprocess.Popen(["python", "log_in_page.py"])
        return
    else:
        error_label.config(text="Invalid username or password")

        # Hide the error message after 3 seconds
        sign_up_page.after(3000, lambda: error_label.config(text=""))


background = "assets/cat.png"
background_image = ImageTk.PhotoImage(Image.open(background))

kat_label = customtkinter.CTkLabel(master=sign_up_page, image=background_image)
kat_label.pack()

frame = customtkinter.CTkFrame(
    master=sign_up_page, width=320, height=400, corner_radius=10)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

error_label = tk.Label(master=frame)
error_label.place(x=60, y=260)

login_label = customtkinter.CTkLabel(
    master=frame, text="Sign Up", font=('Century Gothic', 30))
login_label.place(x=110, y=45)

User_name_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Username')
User_name_box.place(x=50, y=110)

Password_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Password', show='*')
Password_box.place(x=50, y=165)

confirm_password_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Confirm Password', show='*')
confirm_password_box.place(x=50, y=220)

sign_in_button = customtkinter.CTkButton(
    master=frame, width=220, text="Sign Up", command=button_function, corner_radius=6)
sign_in_button.place(x=50, y=275)


sign_up_page.mainloop()
