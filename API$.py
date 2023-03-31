# Import googlemaps and pyttsx3 modules
import time
import googlemaps
import pyttsx3

# Import geopy and math modules for calculating distance
import geopy
import math
from pyquery import PyQuery
import re

# Define a function to calculate the distance between two coordinates using Haversine formula

# Create a pyttsx3 engine object
engine = pyttsx3.init()

engine.say("where do you want to go?")
time.sleep(5)

def cosine_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate the cosine of the central angle between the two points
    cos_c = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)

    # Calculate the distance using the spherical law of cosines
    r = 6371 # Earth radius in kilometers

    # Return the distance in meters
    return math.acos(cos_c) * r * 1000 

# Create a googlemaps client object with your API key
gmaps = googlemaps.Client(key="YOUR APIKEY")

# Use geolocator to get your current location name from your IP address
current_location_name = ""

# Get your destination name from user input
destination_name = ""

# Use gmaps.directions method to get directions from current location to destination
directions = gmaps.directions(current_location_name, destination_name)
print(directions)


# Set a variable to store the current step index
current_step = 0

# Set a variable to store the threshold distance in meters (you can change this value as you like)
threshold_distance = 10

# Loop through the directions list until you reach the end
while current_step < len(directions[0]["legs"][0]["steps"]):
    # Get the next step from the list
    next_step = directions[0]["legs"][0]["steps"][current_step]

    # Get the end location of this step as latitude and longitude values
    end_location_lat = next_step["end_location"]["lat"]
    end_location_lng = next_step["end_location"]["lng"]

    # Use geopy.geocoders.Nominatim class to create a geolocator object
    geolocator = geopy.geocoders.Nominatim(user_agent="my_app")

    # Use geolocator.geocode method to get your current coordinates from your location name
    current_location = geolocator.geocode(current_location_name)
    current_lat = current_location.latitude
    current_lng = current_location.longitude

    # Calculate the distance between your current location and end location using haversine_distance function
    distance = cosine_distance(
        current_lat, current_lng, end_location_lat, end_location_lng)

    # If distance is less than or equal to threshold distance then print and speak that you have reached this checkpoint
    if distance <= threshold_distance:
        print("You have reached this checkpoint.")
        engine.say("You have reached this checkpoint.")
        engine.runAndWait()
        # Increment current step by 1 and continue loop
        current_step += 1
        continue

    else:
            # Print and speak next step as text
        pq = PyQuery(next_step["html_instructions"])
        tag = pq('*')  # Get all the text inside the HTML instructions
        text = tag.text()  # Convert the tag object to a string
        # Replace any tag with an empty string using re.sub function
        text = re.sub(r'<[^>;]+>', '', text)
        text = re.sub(r'Rd', 'Road', text)
        text = re.sub(r'MA', 'Massachussets', text)
        print(text)
        engine.say(text)
        engine.runAndWait()

        # Wait for some time (you can change this value as you like) before checking the distance again
        time.sleep(5)

        # Go back to the beginning of the loop and check the distance again
        continue

# When you reach end of list print and speak final message
print("You have arrived at your destination.")
engine.say("You have arrived at your destination.")
engine.runAndWait()
