import requests
import os
from dotenv import load_dotenv
load_dotenv()
device_token = os.environ['DEVICE_TOKEN']

thread_id = 'b1MLXqVgKgTUUgkmPy8q1rTJGXuoRdjDvqzPHCm0ROP'


def check_message(thread_id):
    headers = {
        'Authorization': f'Bearer {device_token}',
        'Accept': 'application/vnd.allegro.public.v1+json',

    }

    url = f'https://api.allegro.pl/messaging/threads/{thread_id}/messages'

    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()
    else:
        print(
            f"Failed to post the message. Status Code: {response.status_code}")


print(check_message(thread_id))
