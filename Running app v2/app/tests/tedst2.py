from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="main.app")

# Get the user's location based on IP address
ip_address = input("122.56.88.35")  # Optional: Remove this line if you want to use your own IP address
location = geolocator.geocode(query=ip_address)

# Access the location details
print("User's Location:")
print("Latitude:", location.latitude)
print("Longitude:", location.longitude)
print("City:", location.raw['address'].get('city'))
print("Country:", location.raw['address'].get('country'))