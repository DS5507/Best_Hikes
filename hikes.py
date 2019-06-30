# hikes.py

import csv
import json
import os
import webbrowser

from dotenv import load_dotenv
from urllib.request import urlopen
import requests
import datetime
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.

load_dotenv()

hike_key = os.environ.get("hike_key")

print("")
print("")
print("Hey, I'm stoked that you want to go hiking.  Let's find you the best route!")
print("--------------------")

while True:
    print("I'll need your basecamp location to find your best route.")
    street_raw = input("What's your street address? (Ex: 123 Main St): ").lower()
    street = street_raw.replace(" ", "+")
    zipcode = input("How about your zip code? (Ex: 10013): ").lower()
    print("Let me check my map and compass and see if I can find you...")
    print("")

    address_url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street}&zip={zipcode}&benchmark=Public_AR_Current&format=json"
    response_address = requests.get(address_url)
    parsed_response_address = json.loads(response_address.text)
    
    while parsed_response_address['result']['addressMatches'] == []:
        print("There's a little problem... I couldn't find your address.  Why don't you try again?  Pro Tip:  I just need your street address and your zip code, not the city or state.")
        print("--------------------")
        break
    else:
        print(f"Great, I found your starting point!  I'll start my search from: {parsed_response_address['result']['addressMatches'][0]['matchedAddress']}")  
        print("")
        break

while True:
    how_hard = input("On a scale of 1-5, a '1' would be something like a stroll in the park and a '5' is probably better left to more experienced hikers and backpackers. What difficulty level are you interested in?: ").lower()
    while how_hard not in str([1, 2, 3, 4, 5]):
        print("Can you pick something between 1 - 5?")
        print("--------------------")
        how_hard = input("On a scale of 1-5, what difficulty level are you interested in?:  ").lower()
    else:
        print(f"Okay, I'll look for something with a difficulty rating of {how_hard} out of 5")
        print("")

 
    distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()
######## Need to error proof a string
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

## Refactor to 1 for loop?

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


    while selected_trails != []:
        print(f"There's {len(selected_trails)} trails that meet your criteria!")
        print("")
        print("--------------------")
        t = 0
        while True:
            selected_hike_name = selected_trails[t]['name']
            selected_hike_summary = selected_trails[t]['summary']
            selected_hike_length = selected_trails[t]['length']
            selected_hike_rating = selected_trails[t]['stars']
            selected_hike_difficulty_raw = selected_trails[t]['difficulty']
            selected_hike_location = selected_trails[t]['location']
            selected_hike_url_response = selected_trails[t]['url']
            selected_hike_id = selected_trails[t]["id"]
            selected_hike_difficulty = selected_trails[t]["difficulty"]

            print("")
            print(f"I found a great hike for you! You should check out: '{selected_hike_name}'.")
            print(f"The route is {selected_hike_length} miles long and is located in {selected_hike_location}.")
            print(f"The community has given this trail {selected_hike_rating} out of 5 stars.")
            print("")
            print(f"Here's a summary of the trail: {selected_hike_summary}")
            print("")
           
            while True:
                morenew = input(f"Select 'More' for additional options or 'Next' to see the next hike that met your criteria.: ").lower()
                if morenew not in ["more", "next"]:
                    print("Please choose 'More' or 'Next'.")
                    print("")
                else:    
                    if morenew == "next":
                        print("-------------------")
                        if t <= len(selected_trails):
                            t = t+1
                            break
                        else:
                            t = 0
                            print("FYI, you cycled through your whole list.  I'll start at the beginning again.")
                            break
                    elif morenew == "more":
                        print("-------------------")
                        print("")
                        print("")
                        print("Awesome, I'm really excited that you found a hike you like!  I've got a couple of options you can choose from now:")
                        print("Web - View more about the hike you selected on the Hiking Project Website")
                        print("Email - Send an Email with info about your selected hike")
                        print("CSV - Save a list of all of the hikes that met your criteria to a CSV file to your local drive")
                        print("Exit - Wrap it up and hit the trail!")
                        
                        while True:
                            final_choice = input("So go ahead and please choose: 'Web,' 'Email,' 'CSV,' 'Exit': ").lower()
                            if final_choice not in ["web", "email", "csv", "exit"]:
                                print("")
                                print("Please choose: 'Web,' 'Email,' 'CSV,' 'Exit'") 
                            elif final_choice == "web":
                                webbrowser.open_new(selected_hike_url_response)
                                print("Cool, check your browser!")
                                print("")
                            elif final_choice == "email":
                                to_email = input("What email should I send your selected hike to?: ")
                                SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "Oh no!  Please get a sendgrid API key and then put it into the .env file in this directory as 'SENDGRID_API_KEY'")
                                MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "Go in the .env file in this directory and assign an email address to 'MY_EMAIL_ADDRESS'")

                                # AUTHENTICATE

                                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

                                # COMPILE REQUEST PARAMETERS (PREPARE THE EMAIL) 
                                from_email = Email(MY_EMAIL_ADDRESS)
                                to_email = Email(to_email)
                                subject = "Your Next Great Hiking Adventure"

##Collapse output to a single variable

                                #message_text = f"I found a great hike for you! You should check out: '{selected_hike_name}'.\n\n The route is {selected_hike_length} miles long and is located in {selected_hike_location}.\n\n The community has given this trail {selected_hike_rating} out of 5 stars.\n\n\n\n Here's a summary of the trail: {selected_hike_summary}\n\n\n\n Check out more about this route here: {selected_hike_url_response}"
                                message_text = "test"
                                content = Content("text/plain", message_text)
                                mail = Mail(from_email, subject, to_email, content)

                                # ISSUE REQUEST (SEND EMAIL)

                                response = sg.client.mail.send.post(request_body=mail.get())
                                print("Email sent.  Thanks!")
                                print("")

                                ###########
                            elif final_choice == "csv":
                                csv_file_path = os.path.join(os.path.dirname(__file__), "saved_hikes", f"Difficulty_{how_hard}_Within_{distance}_Miles")

                                csv_headers = ["Hike Name", "Rating", "Reference URL"]

                                with open(csv_file_path, "w") as csv_file:
                                    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                                    writer.writeheader() 
                                    for x in selected_trails:
                                        writer.writerow({
                                            "Hike Name": (x['name']),
                                            "Rating": (x['stars']),
                                            "Reference URL": (x['url']),
                                        })
                                print("")
                                print(f"I've saved your list to a .csv file and you can find it at {csv_file_path}.csv")
                                print("")
                            elif final_choice == "exit":
                                exit()
else:
    print("")
    print("Welp, we hit a snag. I couldn't find anything that matched the difficulty and search radius that you provided.  You should try again, but maybe try selecting a different difficulty level or increasing your search radius.  Thanks!")
    print("")
