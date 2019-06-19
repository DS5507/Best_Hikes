# hikes.py

import requests


## User Input
print("Hey, we're stoked that you want to go hiking.  Let's find you the best route!")
print("--------------------")
print("We'll need your basecamp location to find your best route.")
street_raw = input("What's your street address? (Ex: 123 Main St): ").lower()
street = street_raw.replace(" ", "+")
zipcode = input("How about your zip code? (Ex: 10013): ").lower()
distance = input("Just how many miles would you be willing to travel to find the best route?").lower()

# TODO: Add Address Validation
# TODO: Add Additional Options

## Address to Lat/Lon

address_url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street}&zip={zipcode}&benchmark=Public_AR_Current&format=json"
print(address_url)
breakpoint()


## Lat/Lon to Route