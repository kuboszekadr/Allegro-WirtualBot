import json
import requests
import logging

from typing import List

from src.endpoints.auth.Token import Token
from src.models.Message import Message, MessageType


class Thread:
    endpoint = 'https://api.allegro.pl/messaging/threads'

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

    # def get_last_message_from_user(
    #         self, 
    #         user: str
    #     ) -> Message:

    #     msgs_sorted = sorted(
    #         self.msgs,
    #         key=lambda x: x.createdAt,
    #         reverse=True
    #     )

    #     # TODO
    #     # RUN every 5minutes, check if new message arrived
    #     msgs_filtered = filter(
    #         lambda x: \
    #             (x.author.login == user)
    #             # TODO HERE
    #             and (x.type == MessageType.ASK_QUESTION), 
    #         msgs_sorted
    #         )
    #     msgs_filtered = list(msgs_filtered)

    #     if msgs_filtered is None or len(msgs_filtered) == 0:
    #         return None

    #     msg = msgs_filtered[0]
    #     return msg

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
    