import json
import requests
import logging

from typing import List

from src.endpoints.auth.Token import Token
from src.models.Message import Message, MessageType
from src.AppConfig import config

class Thread:

    def __init__(self, id: str, token: Token) -> None:
        self.id: str = id
        self.token: Token = token
        self.msgs: List[Message] = None

    def _headers(self):
        headers = {
            'Authorization': f'Bearer {self.token.value}',
            'Accept': 'application/vnd.allegro.public.v1+json',
            'Content-Type': 'application/vnd.allegro.public.v1+json'
        }
        return headers

    def endpoint(self) -> str:
        result = f'https://api.allegro.pl{config.prefix}/messaging/threads'
        return result

    def get_messages(
            self, 
            limit: int = None, 
            offset: int = None, 
            before: str = None, 
            after: str = None
            ) -> List[Message]:
        
        params = {
            'limit': limit,
            'offset': offset,
            'before': before,
            'after': after
        }
        params = {k: v for k, v in params.items() if v}

        r = requests.get(
            f"{self.endpoint}/{self.id}/messages",
            headers=self._headers(),
            params=params
        )

        results = r.json()['messages']
        results = [Message(**t) for t in results]
        
        self.msgs = results
        return results

    def requires_answer(self, user: str) -> bool:
        msgs_sorted = sorted(
            self.msgs,
            key=lambda x: x.createdAt,
            reverse=True
        )

        last_message = msgs_sorted[0]
        result = last_message.author.login != user
        return result

    def send_message(self, content: str) -> int:
        url = f'{self.endpoint}/{self.id}/messages'

        payload = {
            "text": content,
            "attachments": [],
            "type": "REGULAR"
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
    