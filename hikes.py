# hikes.py

import csv
import json
import os
import webbrowser

from dotenv import load_dotenv
import requests
import datetime
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.

load_dotenv()

hike_key = os.environ.get("hike_key")

print("")
print("")
print("Hey, I'm stoked that you want to go hiking.  Let's find you the best route!")
print("")

while True:
    print("I'll need your basecamp location to find your best route.")
    street_raw = input("What's your street address? (Ex: 40 W 4th St): ").lower()
    street = street_raw.replace(" ", "+")
    zipcode = input("How about your zip code? (Ex: 10012): ").lower()
    print("Let me check my map and compass and see if I can find you...")
    print("")

    address_url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street}&zip={zipcode}&benchmark=Public_AR_Current&format=json"  ## Adapted from Robo Advisor Project
    response_address = requests.get(address_url)
    parsed_response_address = json.loads(response_address.text)
    
    while parsed_response_address['result']['addressMatches'] == []:
        print("There's a little problem... I couldn't find your address.  Why don't you try again?  Pro Tip:  I just need your street address and your zip code, not the city or state.")
        print("")
        break
    else:
        print(f"Great, I found your starting point!  I'll start my search from: {parsed_response_address['result']['addressMatches'][0]['matchedAddress']}")  
        print("")
        break

while True:
    how_hard = input("On a scale of 1-5, a '1' would be something like a stroll in the park and a '5' is probably better left to more experienced hikers and backpackers. What difficulty level are you interested in?: ").lower()
    while how_hard not in str([1, 2, 3, 4, 5]):
        print("Can you pick a whole number between 1 - 5?")
        print("")
        how_hard = input("On a scale of 1-5, what difficulty level are you interested in?:  ").lower()
    else:
        print(f"Okay, I'll look for something with a difficulty rating of {how_hard} out of 5")
        print("")

 
    distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()
    while (distance.isdigit()) == False:  ## Adapted from https://pynative.com/python-check-user-input-is-number-or-string/
        print("Sorry, I really need a whole number between 1 and 200")
        print("")
        distance = input("Just how many miles would you be willing to travel to find the best route? ").lower()
    else:
        distance = int(distance)
    if distance >= 201:
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
    hike_url = f"https://www.hikingproject.com/data/get-trails?lat={lat}&lon={lon}&minStars=3&sort=quality&maxDistance={distance}&maxResults=500&key={hike_key}"  ## Adapted from Robo Advisor Project
    response_hike = requests.get(hike_url)
    parsed_response_hike = json.loads(response_hike.text)
    
    while (parsed_response_hike)['success'] == int(1):
        break
    else:
        print("Welp, we hit a snag. I couldn't get a valid response back from the Hiking Project.  Let's try again.")      
        break

    green_trails = []
    greenBlue_trails=[]
    blue_trails = []
    blueBlack_trails = []
    black_trails = []
    selected_trails = []

    hike_list = (parsed_response_hike)['trails']
    for x in hike_list:  ##  supriyajha5 helped me with the initial list comprehension needs.
        if str(x["difficulty"]) == "green":
            green_trails.append(x)
        elif str(x["difficulty"]) == "greenBlue":
            greenBlue_trails.append(x)
        elif str(x["difficulty"]) == "blue":
            blue_trails.append(x)
        elif str(x["difficulty"]) == "blueBlack":
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
            selected_hike_location = selected_trails[t]['location']
            selected_hike_url_response = selected_trails[t]['url']

            print("")
            def selected_output(selected_trails):
                return(f"I found a great hike for you! You should check out: '{selected_hike_name}'.\n\nThe route is {selected_hike_length} miles long and is located in {selected_hike_location}.\n\nThe community has given this trail {selected_hike_rating} out of 5 stars.\n\nHere's a summary of the trail: {selected_hike_summary}")

            print(selected_output(selected_trails))
            print("")

            while True:
                morenew = input(f"Select 'More' for additional options or 'Next' to see the next hike that met your criteria.: ").lower()
                if morenew not in ["more", "next"]:
                    print("Please choose 'More' or 'Next'.")
                    print("")
                else:    
                    if morenew == "next":
                        print("-------------------")
                        if t < len(selected_trails)-1:
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
                            elif final_choice == "web":  ## Adapted from https://www.csestack.org/code-python-to-open-url-in-browser/
                                webbrowser.open_new(selected_hike_url_response)
                                print("")
                                print("Cool, check your browser!")
                                print("")
                            elif final_choice == "email":  ## Adapted from Shopping Cart Exercise
                                to_email = input("What email should I send your selected hike to?: ")
                                SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "Oh no!  Please get a sendgrid API key and then put it into the .env file in this directory as 'SENDGRID_API_KEY'")
                                MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "Go in the .env file in this directory and assign an email address to 'MY_EMAIL_ADDRESS'")

                                # AUTHENTICATE

                                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

                                # COMPILE REQUEST PARAMETERS (PREPARE THE EMAIL) 
                                from_email = Email(MY_EMAIL_ADDRESS)
                                to_email = Email(to_email)
                                subject = "Your Next Great Hiking Adventure"

                                message_text = f"{selected_output(selected_trails)}\n\nCheck out more about this route here: {selected_hike_url_response}"

                                content = Content("text/plain", message_text)
                                mail = Mail(from_email, subject, to_email, content)

                                # ISSUE REQUEST (SEND EMAIL)
                                response = sg.client.mail.send.post(request_body=mail.get())
                                print("")
                                print("Great, I sent off all the info!")
                                print("")

                            elif final_choice == "csv":  ## Adapted from Robo Advisor Exercise
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
