import requests
import json
import logging


class Threads:
    endpoint = 'https://api.allegro.pl/messaging/threads'

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    @property
    def _headers(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
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

        r  = requests.post(
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
        return results

    def get(self, thread_id: str) -> dict:
        r = requests.get(
            f"{self.endpoint}/{thread_id}",
            headers=self._headers,
        )
        result = r.json()
        return result

if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.getcwd())
    
    from src.auth.OAuth import OAuth
    from dotenv import load_dotenv

    load_dotenv()
    oauth = OAuth(
        client_id = os.environ['CLIENT_ID'],
        client_secret= os.environ['CLIENT_SECRET']
    )
    token = oauth.token[0]

    threads = Threads(access_token=token)

    threads_list = threads.thread_list
    thread = threads.get(threads_list[0]['id'])
    pass