import requests
import json
import os
import logging
from dotenv import load_dotenv
load_dotenv()


def post_auto_message(thread_id):
    device_token = os.environ['DEVICE_TOKEN']
    headers = {
        'Authorization': f'Bearer {device_token}',
        'Accept': 'application/vnd.allegro.public.v1+json',
        'Content-Type': 'application/vnd.allegro.public.v1+json'
    }

    data = {
        "text": 'Hej Mordeczko, nasz asystent odpowie wkrótce',
        "attachments": [],
        "type": "REGULAR"
    }

    url = f'https://api.allegro.pl/messaging/threads/{thread_id}/messages'

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.ok:
        logging.info("Message posted successfully.")
    else:
        logging.error(
            f"Failed to post the message. Status Code: {response.status_code}")
