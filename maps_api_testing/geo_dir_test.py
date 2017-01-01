import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBgqtZncNpVtWhVJOGCzUrzEZrivxU8z5g')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("230 Mallard Drive",
                                     "Monroeville, PA",
                                      mode="walking",
                                      departure_time=now)




print(directions_result)
