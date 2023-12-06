import requests
import json
from get_last_disp_id import get_last_dispute_id
from get_token import get_token

dispute_id = get_last_dispute_id()


def post_auto_message(dispute_id, message_type="REGULAR"):
    headers = {
        'Authorization': f'Bearer {get_token()}',
        'Accept': 'application/vnd.allegro.public.v1+json',
        'Content-Type': 'application/vnd.allegro.public.v1+json'
    }

    data = {
        "text": 'Hej Mordeczko, nasz asysten odpowie wkrótce',
        "type": message_type
    }

    url = f'https://api.allegro.pl/sale/disputes/{dispute_id}/messages'

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.ok:
        print("Message posted successfully.")
    else:
        print(
            f"Failed to post the message. Status Code: {response.status_code}")

# Example usage
