import geocoder

g = geocoder.ip("me")

print("your lat and long is", g.latlng)
