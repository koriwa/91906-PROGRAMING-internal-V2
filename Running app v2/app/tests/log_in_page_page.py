# importing required modules
import tkinter
import customtkinter
from PIL import ImageTk, Image

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("system")
# Themes of customtkinter which are blue green black
customtkinter.set_default_color_theme("blue")

sign_in_page = customtkinter.CTk()  # creating a window
sign_in_page.resizable(width=False, height=False)
sign_in_page.title('Login')  # frame window name


def button_function_login():
    # destroy current window exiting the loop so it creates a new one
    sign_in_page.destroy()
    import tests.home_page as home_page
    
def button_function_signup():
    # destroy current window exiting the loop so it creates a new one
    sign_in_page.destroy()
    import sign_up_page

# making/adding a background image so it doesn't look plain

background = (r"G:\My Drive\main app\app\assets\Untitled-2.png")
background_image = ImageTk.PhotoImage(Image.open(background))
kat_label = customtkinter.CTkLabel(master=sign_in_page, image=background_image, width=1000, height=1000)
kat_label.pack()


# creating the frame, sign in(username and password box)
frame = customtkinter.CTkFrame(
    master=kat_label, width=320, height=400, corner_radius=30, fg_color="transparent", bg_color="transparent")
# relax and rely are basically the horizontal and vertical offaset as a float
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  # master = root

login_label = customtkinter.CTkLabel(
    master=frame, text="Log into your Account", font=('Century Gothic', 20))
login_label.place(x=65, y=45)

User_name_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Username')
User_name_box.place(x=50, y=110)

Password_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Password', show="*")  # makign the pass show **** instead of your password
Password_box.place(x=50, y=165)

# creating buttons for google and facebook sign in

login_button = customtkinter.CTkButton(
    master=frame, width=220, text="Login", command=button_function_login, corner_radius=6)
login_button.place(x=50, y=220)

sign_in_button = customtkinter.CTkButton(
    master=frame, width=220, text="Sign Up", command=button_function_signup, corner_radius=6)
sign_in_button.place(x=50, y=270)

facebook_img = (r"G:\My Drive\main app\app\assets\facebookimg.png")

google_img = (r"G:\My Drive\main app\app\assets\Google__G__Logo.svg.webp")


google_image = customtkinter.CTkImage(Image.open(
    google_img).resize((20, 20), Image.LANCZOS))


facebook_image = customtkinter.CTkImage(Image.open(
    facebook_img).resize((20, 20), Image.LANCZOS))


google_button = customtkinter.CTkButton(master=frame, image=google_image, text="Google", width=100,
                                        height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
google_button.place(x=50, y=320)


facebook_button = customtkinter.CTkButton(master=frame, image=facebook_image, text="Facebook", width=100,
                                          height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
facebook_button.place(x=170, y=320)


sign_in_page.mainloop()
