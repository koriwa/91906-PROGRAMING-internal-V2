import tkinter as tk
import tkinter.ttk as ttk
import time
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        self.is_running = False
        self.start_time = None
        self.distance = 0.0

        self.style = ttk.Style()
        self.style.configure("Timer.TLabel", font=("Arial", 24), padding=10)
        self.style.configure("Distance.TLabel", font=("Arial", 18), padding=5)

        self.distance_label = ttk.Label(root, text="Distance: 0.0 km", style="Distance.TLabel")
        self.distance_label.pack()

        self.timer_label = ttk.Label(root, text="00:00:00", style="Timer.TLabel")
        self.timer_label.pack()

        self.start_button = ttk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack()

        self.geocoder = OpenCageGeocode('1370879a48ca402aa424b1092605c2ca')  # Replace with your OpenCage API key

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_timer()

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            elapsed_time = time.time() - self.start_time
            distance = self.calculate_distance(elapsed_time)
            self.distance += distance
            self.update_distance_label()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            timer_str = self.format_time(elapsed_time)
            self.timer_label.config(text=timer_str)
            self.root.after(1000, self.update_timer)

    def format_time(self, elapsed_time):
        hours = int(elapsed_time / 3600)
        minutes = int((elapsed_time % 3600) / 60)
        seconds = int((elapsed_time % 3600) % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def calculate_distance(self, elapsed_time):
        start_location = self.get_user_location()
        current_location = self.get_user_location()
        if start_location and current_location:
            start_coordinates = (start_location[0], start_location[1])
            current_coordinates = (current_location[0], current_location[1])
            distance = geodesic(start_coordinates, current_coordinates).kilometers
            return distance
        else:
            return 0.0

    def get_user_location(self):
        try:
            results = self.geocoder.geocode("")  # Replace with your desired location or leave it empty for automatic IP-based location
            if len(results) > 0:
                latitude = results[0]['geometry']['lat']
                longitude = results[0]['geometry']['lng']
                print("Latitude:", latitude)
                print("Longitude:", longitude)
                return latitude, longitude
            else:
                return None
        except Exception as e:
            print("Error retrieving user location:", e)
            return None

    def update_distance_label(self):
        self.distance_label.config(text=f"Distance: {self.distance:.2f} km")

root = tk.Tk()
app = TimerApp(root)
root.mainloop()
