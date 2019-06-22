# hikes.py

import csv
import json
import os


from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

hike_key = os.environ.get("hike_key")

print("Hey, I'm stoked that you want to go hiking.  Let's find you the best route!")
print("--------------------")

while True:
    ## User Input

    print("We'll need your basecamp location to find your best route.")
    street_raw = input("What's your street address? (Ex: 123 Main St): ").lower()
    street = street_raw.replace(" ", "+")
    zipcode = input("How about your zip code? (Ex: 10013): ").lower()
    print("Let me check my map and compass and see if I can find you...")
    print("--------------------")

    # TODO: Add Additional Options

    ## Address to Lat/Lon
    address_url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street}&zip={zipcode}&benchmark=Public_AR_Current&format=json"
    response_address = requests.get(address_url)
    parsed_response_address = json.loads(response_address.text)
    
    while parsed_response_address['result']['addressMatches'] == []:
        print("There's a little problem... we couldn't find your address.  Why don't you try again?  Pro Tip:  We just need your street address and your zip code, not the city or state.")
        print("--------------------")
        break
    else:
        print("Great, we found your starting point!")  
        break

distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()
if float(distance) >= 201:
    print("Sorry, I can only look 200 miles in any direction.  I'll go ahead and look 200 miles out for you though!")
    distance = 200
else:
    pass

print("Okay, just a sec while we find something awesome for you.")

matched_address = parsed_response_address['result']['addressMatches'][0]['matchedAddress']
coordinates = parsed_response_address['result']['addressMatches'][0]['coordinates']
lat = parsed_response_address['result']['addressMatches'][0]['coordinates']['y'] 
lon = parsed_response_address['result']['addressMatches'][0]['coordinates']['x']

## Lat/Lon to Route
hike_url = f"https://www.hikingproject.com/data/get-trails?lat={lat}&lon={lon}&minStars=3&sort=quality&maxDistance={distance}&maxResults=5&key={hike_key}"
response_hike = requests.get(hike_url)
parsed_response_hike = json.loads(response_hike.text)
hike_list = (parsed_response_hike)['trails']
hike_name = (parsed_response_hike)['trails'][0]['name']
hike_summary = (parsed_response_hike)['trails'][0]['summary']
hike_length = (parsed_response_hike)['trails'][0]['length']
hike_rating = (parsed_response_hike)['trails'][0]['stars']
hike_difficulty_raw = (parsed_response_hike)['trails'][0]['difficulty']
hike_location = (parsed_response_hike)['trails'][0]['location']
hike_url_response = (parsed_response_hike)['trails'][0]['url']
hike_id = (parsed_response_hike)['trails'][0]["id"]


if hike_difficulty_raw == "green":
    hike_difficulty = "Easy"
elif hike_difficulty_raw == "greenBlue":
    hike_difficulty = "Moderately Easy"    
elif hike_difficulty_raw == "blue":
    hike_difficulty = "Moderate"
elif hike_difficulty_raw == "blueBlack":
    hike_difficulty = "Moderately Hard"
else:
    hike_difficulty = "Hard"

print("--------------------")
print(f"We found a great hike for you! The highest rated route within {distance} miles is named '{hike_name}'.")
print(f"The route is {hike_length} miles long and is located in {hike_location}.")
print(f"The community has given this trail {hike_rating} out of 5 stars and labeled its diffulty as {hike_difficulty}.")
print(f"Here's a summary of the trail: {hike_summary}")
print(f"You can check out more about this hike at {hike_url_response}.")

green_list = []
greenBlue_list=[]
blue_list = []
blueBlack_list = []
black_list = []


for x in hike_list:
    if str(x["difficulty"]) == "green":
        blueBlack_list.append(x["id"]) 
    elif str(x["difficulty"]) == "greenBlue":
        greenBlue_list.append(x["id"]) 
    elif str(x["difficulty"]) == "blue":
        blue_list.append(x["id"]) 
    elif str(x["difficulty"]) == "blueBlack":
        blueBlack_list.append(x["id"]) 
    else:
        black_list.append(x["id"]) 

green_trails = []
greenBlue_trails=[]
blue_trails = []
blueBlack_trails = []
black_trails = []

for x in hike_list:
    if str(x["id"]) in str(green_list):
        green_trails.append(x)
    elif str(x["id"]) in str(greenBlue_list):
        greenBlue_trails.append(x)
    elif str(x["id"]) in str(blue_list):
        blue_trails.append(x)
    elif str(x["id"]) in str(blueBlack_list):
        blueBlack_trails.append(x)
    else:
        black_list.append(x)





breakpoint()

# TODO: What is no trails?