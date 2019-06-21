# hikes.py

import csv
import json
import os


from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

hike_key = os.environ.get("hike_key")

print("Hey, we're stoked that you want to go hiking.  Let's find you the best route!")
print("--------------------")

while True:
    ## User Input

    print("We'll need your basecamp location to find your best route.")
    street_raw = input("What's your street address? (Ex: 123 Main St): ").lower()
    street = street_raw.replace(" ", "+")
    zipcode = input("How about your zip code? (Ex: 10013): ").lower()



    # TODO: Add Additional Options

    ## Address to Lat/Lon
    address_url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street}&zip={zipcode}&benchmark=Public_AR_Current&format=json"
    response_address = requests.get(address_url)
    parsed_response_address = json.loads(response_address.text)

    while parsed_response_address['result']['addressMatches'] == []:
        print("There's a little problem... we couldn't find your address.  Why don't you try again?  Pro Tip:  We just need your street address and your zip code, not the city or state.")
        break
    else:
        print("Great, we found your starting point!")
        break

distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()

matched_address = parsed_response_address['result']['addressMatches'][0]['matchedAddress']
coordinates = parsed_response_address['result']['addressMatches'][0]['coordinates']
lat = parsed_response_address['result']['addressMatches'][0]['coordinates']['y'] 
lon = parsed_response_address['result']['addressMatches'][0]['coordinates']['x']

## Lat/Lon to Route
hike_url = f"https://www.hikingproject.com/data/get-trails?lat={lat}&lon={lon}&minStars=3&sort=quality&maxDistance={distance}&key={hike_key}"
response_hike = requests.get(hike_url)
parsed_response_hike = json.loads(response_hike.text)
hike_name = (parsed_response_hike)['trails'][0]['name']
hike_summary = (parsed_response_hike)['trails'][0]['name']
hike_length = (parsed_response_hike)['trails'][0]['length']
hike_rating = (parsed_response_hike)['trails'][0]['stars']
hike_difficulty_raw = (parsed_response_hike)['trails'][0]['difficulty']
hike_location = (parsed_response_hike)['trails'][0]['location']

if hike_difficulty_raw == "green":
    hike_difficulty = "Easy"
elif hike_difficulty_raw == "Black":
    hike_difficulty = "Hard"
else:
    hike_difficulty = "Moderate"
print("--------------------")
print(f"We found a great hike for you! The highest rated route within {distance} miles is named '{hike_name}'.")
print(f"The route is {hike_length} miles long and is located in {hike_location}.")
print(f"The community has given this trail {hike_rating} out of 5 stars and labeled its diffulty as {hike_difficulty}.")
print(f"Here's a summary of the trail: {hike_summary}.")
