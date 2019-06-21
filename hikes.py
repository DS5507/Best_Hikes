# hikes.py

import csv
import json
import os


from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

hike_key = os.environ.get("hike_key")


## User Input
print("Hey, we're stoked that you want to go hiking.  Let's find you the best route!")
print("--------------------")
print("We'll need your basecamp location to find your best route.")
street_raw = input("What's your street address? (Ex: 123 Main St): ").lower()
street = street_raw.replace(" ", "+")
zipcode = input("How about your zip code? (Ex: 10013): ").lower()
distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()

# TODO: Add Address Validation
# TODO: Add Additional Options

## Address to Lat/Lon
address_url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street}&zip={zipcode}&benchmark=Public_AR_Current&format=json"
response_address = requests.get(address_url)
parsed_response_address = json.loads(response_address.text)

matched_address = parsed_response_address['result']['addressMatches'][0]['matchedAddress']
coordinates = parsed_response_address['result']['addressMatches'][0]['coordinates']
lat = parsed_response_address['result']['addressMatches'][0]['coordinates']['y'] 
lon = parsed_response_address['result']['addressMatches'][0]['coordinates']['x']

## Lat/Lon to Route
hike_url = f"https://www.hikingproject.com/data/get-trails?lat={lat}&lon={lon}&minStars=3&sort=quality&maxDistance={distance}&key={hike_key}"
response_hike = requests.get(hike_url)
parsed_response_hike = json.loads(response_hike.text)
hike_name = (parsed_response_hike)['trails'][0]['name']
print(f"We found a great hike for you named '{hike_name}''")

breakpoint()