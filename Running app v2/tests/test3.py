import tkinter as tk
import geocoder

def get_location():
    location = geocoder.ip('me')

    if location.ok:
        latitude = location.lat
        longitude = location.lng
        address = location.address
        # Update the label with the user's location
        location_label.config(text=f"Latitude: {latitude}\nLongitude: {longitude}\nAddress: {address}")
    else:
        location_label.config(text="Location not found.")

window = tk.Tk()
window.title("Location Tracker")

track_button = tk.Button(window, text="Track Location", command=get_location)
track_button.pack(pady=10)

location_label = tk.Label(window, text="Press the 'Track Location' button to get your location.")
location_label.pack(pady=10)

window.mainloop()
