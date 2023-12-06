import requests
import os
import logging
from dotenv import load_dotenv
load_dotenv()
device_token = os.environ['DEVICE_TOKEN']


def get_messaging_threads():

    url = 'https://api.allegro.pl/messaging/threads?limit=2'
# Set up the headers with the token and the required Accept header
    headers = {
        'Authorization': f'Bearer {device_token}',
        'Accept': 'application/vnd.allegro.public.v1+json'
    }

    # Make the GET request
    response = requests.get(
        f'{url}',
        headers=headers
    )

    # Check if the request was successful
    if response.ok:

        return response.json()
    else:
        logging.error(
            f"Failed to retrieve data. Status Code: {response.status_code}")


print(get_messaging_threads().get('threads'))
