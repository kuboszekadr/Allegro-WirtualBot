import requests
import json
import logging
import os


class Threads:
    endpoint = 'https://api.allegro.pl/messaging/threads'

    def __init__(self, device_token: str) -> None:
        self.device_token = device_token

    @property
    def _headers(self):
        headers = {
            'Authorization': f'Bearer {self.device_token}',
            'Accept': 'application/vnd.allegro.public.v1+json',
            'Content-Type': 'application/vnd.allegro.public.v1+json'
        }
        return headers

    def send_message(self, dispute_id: str, content: str):
        url = f'{self.endpoint}/{dispute_id}/messages'

        payload = {
            "text": content,
            "attachments": [],
            "type": "REGULAR"
        }

        r = requests.post(
            url,
            headers=self._headers,
            data=json.dumps(payload)
        )

        if not r.ok:
            logging.error(
                f"Failed to post the message. Status Code: {r.status_code}")
            return

        logging.info("Message posted successfully.")

    @property
    def thread_list(self, limit: int = 5) -> dict:
        r = requests.get(
            self.endpoint,
            headers=self._headers,
            params={'limit': limit}
        )

        results = None
        if not r.ok:
            logging.error(
                f"Failed to retrieve data. Status Code: {r.status_code}")
            return results

        results = r.json()['threads']
        with open('./.Threads.json', 'w') as f:
            json.dump(results, f)

        return results
