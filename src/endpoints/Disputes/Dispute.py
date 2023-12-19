import json
import requests
import logging

from typing import List

from src.endpoints.auth.Token import Token
from src.models.Dispute import Dispute


class Disputes:
    endpoint = 'https://api.allegro.pl/sale/disputes'

    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.disputes: List[Dispute] = None

    def _headers(self):
        headers = {
            'Authorization': f'Bearer {self.token.value}',
            'Accept': 'application/vnd.allegro.public.v1+json',
            'Content-Type': 'application/vnd.allegro.public.v1+json'
        }
        return headers

    def get_disputes(
            self, 
            limit: int = None, 
            offset: int = None
            ) -> List[Dispute]:
        
        params = {
            'limit': limit,
            'offset': offset
        }
        params = {k: v for k, v in params.items() if v}

        r = requests.get(
            self.endpoint,
            headers=self._headers(),
            params=params
        )

        results = r.json()['disputes']
        results = [Dispute(**d) for d in results]
        
        self.disputes = results
        return results

    def add_message(self, dispute_id: str, content: str) -> None:
        url = f'{self.endpoint}/{dispute_id}/messages'

        payload = {
            "text": content
        }

        r = requests.post(
            url,
            headers=self._headers(),
            data=json.dumps(payload)
        )

        if not r.ok:
            logging.error(
                f"Failed to post the message. Status Code: {r.status_code}")

        logging.info("Message posted successfully.")
        return