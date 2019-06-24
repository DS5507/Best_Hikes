# hikes.py

import csv
import json
import os
import webbrowser


from dotenv import load_dotenv
from urllib.request import urlopen
import requests
import datetime

load_dotenv()

printtime = '{0:%Y-%m-%d-%H-%M-%S-%f}'.format(datetime.datetime.now())
hike_key = os.environ.get("hike_key")

print("")
print("")
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
        print(f"Great, I found your starting point!  I'll start my search from: {parsed_response_address['result']['addressMatches'][0]['matchedAddress']}")  
        print("")
        break


while True:
    
    how_hard = input("On a scale of 1-5, a '1' would be something like a stroll in the park and a '5' is probably better left to more experienced hikers and backpackers. What difficulty level are you interested in? : ").lower()
    while how_hard not in str([1, 2, 3, 4, 5]):
        print("Can you pick something between 1 - 5?")
        print("--------------------")
        how_hard = input("On a scale of 1-5, what difficulty level are you interested in? ").lower()
    else:
        print(f"Okay, I'll look for something with a difficulty rating of {how_hard} out of 5")
        print("")

 
    distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()
    if float(distance) >= 201:
        print("Sorry, I can only look 200 miles in any direction.  I'll go ahead and look 200 miles out for you though!")
        distance = 200

    print("Okay, just a sec while I try to find something awesome for you.")
    print("--------------------")
    print("")


    matched_address = parsed_response_address['result']['addressMatches'][0]['matchedAddress']
    coordinates = parsed_response_address['result']['addressMatches'][0]['coordinates']
    lat = parsed_response_address['result']['addressMatches'][0]['coordinates']['y'] 
    lon = parsed_response_address['result']['addressMatches'][0]['coordinates']['x']

    ## Lat/Lon to Route
    hike_url = f"https://www.hikingproject.com/data/get-trails?lat={lat}&lon={lon}&minStars=3&sort=quality&maxDistance={distance}&maxResults=500&key={hike_key}"
    response_hike = requests.get(hike_url)
    parsed_response_hike = json.loads(response_hike.text)
    

    while (parsed_response_hike)['success'] == int(1):
        break
    else:
        print("Welp, we hit a snag. I couldn't get a valid response back from the Hiking Project.  Let's try again.")      
        break

    hike_list = (parsed_response_hike)['trails']
    hike_name = (parsed_response_hike)['trails'][0]['name']
    hike_summary = (parsed_response_hike)['trails'][0]['summary']
    hike_length = (parsed_response_hike)['trails'][0]['length']
    hike_rating = (parsed_response_hike)['trails'][0]['stars']
    hike_difficulty_raw = (parsed_response_hike)['trails'][0]['difficulty']
    hike_location = (parsed_response_hike)['trails'][0]['location']
    hike_url_response = (parsed_response_hike)['trails'][0]['url']
    hike_id = (parsed_response_hike)['trails'][0]["id"]

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
    selected_trails = []

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
            black_trails.append(x)


    if how_hard == str(1):
        selected_trails = green_trails
    elif how_hard == str(2):
        selected_trails = greenBlue_trails
    elif how_hard == str(3):
        selected_trails = blue_trails
    elif how_hard == str(4):
        selected_trails = blueBlack_trails
    elif how_hard == str(5):
        selected_trails = black_trails
    else:
        pass


    if selected_trails != []:
        t = 0
        selected_hike_name = selected_trails[0]['name']
        selected_hike_summary = selected_trails[0]['summary']
        selected_hike_length = selected_trails[0]['length']
        selected_hike_rating = selected_trails[0]['stars']
        selected_hike_difficulty_raw = selected_trails[0]['difficulty']
        selected_hike_location = selected_trails[0]['location']
        selected_hike_url_response = selected_trails[0]['url']
        selected_hike_id = selected_trails[0]["id"]
        selected_hike_difficulty = selected_trails[0]["difficulty"]


        print(f"There's {len(selected_trails)} trails that meet your criteria!")
        print("")
        print("--------------------")
        print("")
        print(f"We found a great hike for you! The highest rated route that's a {how_hard} out of 5 difficutly and within {distance} miles is named '{selected_hike_name}'.")
        print(f"The route is {selected_hike_length} miles long and is located in {selected_hike_location}.")
        print(f"The community has given this trail {selected_hike_rating} out of 5 stars.")
        print(f"Here's a summary of the trail: {selected_hike_summary}")
        print(f"You can check out more about this hike at {selected_hike_url_response}.")
        
        
        csv_file_path = os.path.join(os.path.dirname(__file__), "saved_hikes", f"Difficulty_{how_hard}_Within_{distance}_Miles")

        csv_headers = ["Hike Name", "Rating", "Reference URL"]

        with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader() # uses fieldnames set above
            for x in selected_trails:
                writer.writerow({
                    "Hike Name": (x['name']),
                    "Rating": (x['stars']),
                    "Reference URL": (x['url']),
        })
        print("")
        print(f"BTW, I went ahead and saved all of the hikes that met your criteria to a .csv file.")  
        print(f"You can find it at {csv_file_path}.csv")
        print("")

        while True:
            view_web = input(f"Do you want to view more about the hike that I selected for you on the Hiking Project?: ").lower()
            while view_web not in ['yes', 'no']:
                print("Sorry, but that was just a 'yes' or 'no' question.")
                break
            else:
                if view_web == "yes":
                    webbrowser.open_new(selected_hike_url_response)
                    exit()
                else:
                    exit()
    else:
        print("")
        print("Welp, we hit a snag. I couldn't find anything that matched the difficulty and search radius that you provided.  You should try again, but maybe try selecting a different difficulty level or increasing your search radius.  Thanks!")
        print("")

