import tkinter as tk

root = tk.Tk()

# Create a transparent label
label = tk.Label(root, text="Transparent Label")
label.config(fg="black")

# Load an image with a transparent background
image = tk.PhotoImage(file="assets/transparent_bg.png")
label.config(image=image)
label.image = image  # Store a reference to the image

label.pack()

root.mainloop()