from tkinter import *
from tkinter import ttk
import gpsd

root = Tk()

gpsd.connect()

packet = gpsd.get_current()
print(packet.position()[0])
print(packet.position()[1])
root.mainloop()