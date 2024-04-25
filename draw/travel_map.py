# script to draw the map with travel location
import folium
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the Excel file
file_path = "/Users/hu/Downloads/Bay Area Things - for Reddit.xlsx"
data = pd.read_excel(file_path, engine="openpyxl")


def get_places_list(data, column_name):
    places_list = data[column_name].dropna().unique().tolist()
    return places_list


def get_location(place_name, geolocator):
    try:
        location = geolocator.geocode(place_name + ", Bay Area, California")
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Error geocoding {place_name}: {e}")
        return None


def main(data):
    column_name = "The Thing"
    places_to_visit = get_places_list(data, column_name)
    print(places_to_visit)
    current_location = (37.7749, -122.4194)  # San Francisco City Center

    geolocator = Nominatim(user_agent="geoapiExercises")
    geocode = RateLimiter(
        geolocator.geocode, min_delay_seconds=1
    )  # rate limiting the geocode calls

    map = folium.Map(location=current_location, zoom_start=10)
    folium.Marker(
        current_location, popup="Current Location", icon=folium.Icon(color="red")
    ).add_to(map)

    for place in places_to_visit:
        loc = get_location(place, geocode)
        if loc:
            distance = geodesic(current_location, loc).miles
            popup_info = f"{place}: {distance:.2f} miles"
            folium.Marker(loc, popup=popup_info, icon=folium.Icon(color="blue")).add_to(
                map
            )
        else:
            print(f"Location not found: {place}")
        time.sleep(1)  # sleep to prevent hitting the API rate limit

    map.save("map.html")


if __name__ == "__main__":
    main(data)
