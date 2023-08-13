import requests
from tkinter import *
from tkinter import ttk
import webbrowser
import threading
from geopy.geocoders import Nominatim

root = Tk()
root.title("Timer App")
root.geometry("495x595")

# Replace with your actual values
GOOGLE_CLIENT_ID = "1097287749447-lutelaoi15qk923thbcqd5mn0dttnfg6.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8000/auth"
GOOGLE_MAPS_API_KEY = "AIzaSyABK7Jhl0R1R-rxDN0qK8YiUSqaxBavs5U"
GOOGLE_CLIENT_SECRET = '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'

# Construct the authentication URL
auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
access_token = None
server = None


def get_public_ip():
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        ip_address = data['query']
        return ip_address
    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


def track_gps(ip_address):
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}"
    payload = {
        "considerIp": False,
        "wifiAccessPoints": [],
        "cellTowers": [],
        "fallbacks": {
            "ipGeoLocation": True
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        print(data)

        if 'location' in data and 'lat' in data['location'] and 'lng' in data['location']:
            latitude = data["location"]["lat"]
            longitude = data["location"]["lng"]
            return latitude, longitude, data
        else:
            print("Latitude and longitude not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def exchange_code_for_token(code):
    try:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,  # Replace with your client secret
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)
        response_data = response.json()

        if 'access_token' in response_data:
            global access_token
            access_token = response_data["access_token"]
            start_timer()  # Start the timer
        else:
            print("Token exchange failed.")
            if 'error' in response_data:
                error_message = response_data['error_description']
                print(f"Error message: {error_message}")

    except requests.exceptions.RequestException as e:
        print("Token exchange failed.")
        print(f"An error occurred: {e}")


def fetch_user_profile():
    if access_token:
        profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(profile_url, headers=headers)
            if response.status_code == 200:
                profile_data = response.json()
                print("User Profile:")
                print(f"Name: {profile_data['name']}")
                print(f"Email: {profile_data['email']}")
            else:
                print("Failed to fetch user profile.")
                if 'error' in response.json():
                    error_message = response.json()['error']
                    print(f"Error message: {error_message}")
        except requests.exceptions.RequestException as e:
            print("Failed to fetch user profile.")
            print(f"An error occurred: {e}")
    else:
        print("Access token not available.")


def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"


def start_timer():
    global elapsed_time, is_running
    is_running = True
    timer_tick()


def stop_timer():
    global is_running

    if is_running:
        if access_token:
            result = track_gps(get_public_ip())

            if result:
                latitude, longitude, data = result
                print(f"Latitude: {latitude}")
                print(f"Longitude: {longitude}")
                print("Google Maps API Response:")
                print(data)

                geolocator = Nominatim(user_agent="timer-app")
                location = geolocator.reverse(f"{latitude}, {longitude}")
                if location:
                    address = location.address
                    print(f"Address: {address}")
                else:
                    print("Failed to obtain location address.")
            else:
                print("GPS tracking failed.")
        else:
            print("Failed to obtain the access token.")

        fetch_user_profile()

    is_running = False


def timer_tick():
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        timer_label.config(text=format_time(elapsed_time))
    timer_label.after(10, timer_tick)


elapsed_time = 0
is_running = False

timer_label = ttk.Label(root, text="00:00:00:000", font=("Arial", 20))
timer_label.pack(pady=10)


def start_auth_flow():
    global server
    server = threading.Thread(target=start_flask_server)
    server.start()
    webbrowser.open(auth_url)


def start_flask_server():
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/auth', methods=['GET'])
    def auth_callback():
        # Get the authorization code from the query parameters
        code = request.args.get('code')
        exchange_code_for_token(code)  # Exchange the code for an access token
        server.join()  # Wait for the Flask server to finish
        root.quit()  # Exit the application
        return 'Authorization successful!'  # Respond with a success message

    app.run(port=8000)


start_button = ttk.Button(
    root, text="Start", width=10, command=start_auth_flow)
start_button.pack(side=LEFT, padx=10)

stop_button = ttk.Button(root, text="Stop", width=10, command=stop_timer)
stop_button.pack(side=LEFT)


root.mainloop()
