from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_client_token():

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    # Perform HTTP Basic Authentication
    auth = HTTPBasicAuth(client_id, client_secret)

    # Set the grant type for client credentials
    payload = {
        'grant_type': 'client_credentials'
    }

    # Make the POST request
    response = requests.post(
        'https://allegro.pl/auth/oauth/token',
        auth=auth,
        data=payload
    )

    # Check if the request was successful
    if response.ok:
        # Parse the access token from the response
        return response.json()['access_token']
        # print(f"Access Token: {access_token}")
    else:
        print(
            f"Failed to retrieve the access token. Status Code: {response.status_code}")
