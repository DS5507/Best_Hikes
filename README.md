# Best_Hikes

[Project Description](https://github.com/prof-rossetti/nyu-info-2335-201905/tree/master/projects/freestyle)

## Installation
Clone or download from [GitHub source](https://github.com/DS5507/Best_Hikes), then navigate into the project repository from the command line.

```sh
cd ~\Best_Hikes
```

## App Credentials
Create a copy of ".env.example" and rename it ".env".  

Sendgrid:
Sign up for a free [Sengrid account](https://signup.sendgrid.com/), verify your account, and then create an API Key with "full access" permissions.  Set the environment variables in the .env file to reflect your API key and the email associated with your account.

```
SENDGRID_API_KEY="demo" # use your own API Key!
MY_EMAIL_ADDRESS="Address@Email.Com" # use the email address you associated with the SendGrid service
```

The Hiking Project:
Sign up for a free [Hiking Project account](https://www.hikingproject.com/data) and retrieve your API key.  Set the environment variable in the .env file to reflect your API key.

```
hike_key = "demo" # use your own API Key
```


## Create Virtual Environment
Create a virtual environment from the command line.
```sh
conda create -n hike-env #first time only
conda activate hike-env
```

## Install Requirements
Install the requirements list from the command line.
```sh
pip install -r requirements.txt
```

## Usage
Run the program using the command line.
```sh
python hikes.py
```