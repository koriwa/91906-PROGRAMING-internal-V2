import tkinter as tk


def make_frame_translucent(root):
    # Adjust the alpha value as desired (0.0 to 1.0)
    root.attributes("-alpha", 0.5)


root = tk.Tk()

# Create a frame
frame = tk.Frame(root, width=200, height=200, bg='white')
frame.pack()

# Make the root window translucent
make_frame_translucent(root)

root.mainloop()
