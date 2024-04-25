import pickle

filepath = "./draw/photos_with_location.pkl"
with open(filepath, "rb") as f:
    photos_with_location = pickle.load(f)

# parse the data
import datetime
import matplotlib.pyplot as plt

# dict with uuid as key, location and date as value
# example ## output example:(35.19540333333333, -106.43543) 2023-11-26 17:01:29.422000-07:00
for photo in photos_with_location.values():
    print(type(photo["date"]))
    break

# save to a location list ordered by date
location_date_list = [
    (photo["location"], photo["date"]) for photo in photos_with_location.values()
]
location_date_list.sort(key=lambda x: x[1])
# get the only location list
location_list = [location for location, _ in location_date_list]

import folium
from folium.plugins import HeatMap

# Assuming `locations` is a list of (latitude, longitude) tuples
map = folium.Map(location=[20.0, 0.0], zoom_start=2)
HeatMap(location_list).add_to(map)
map.save("heatmap.html")
