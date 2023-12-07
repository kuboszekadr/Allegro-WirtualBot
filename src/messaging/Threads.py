import requests
import json
import logging
import os

from typing import List, Any


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
            return r

        results = r.json()['threads']
        with open('./.Threads.json', 'w') as f:
            json.dump(results, f)

        return results

    def get(self, thread_id: str) -> dict:
        r = requests.get(
            f"{self.endpoint}/{thread_id}",
            headers=self._headers,
        )
        result = r.json()
        return result

    def list_messages(self, thread_id: str, limit: int = None, offset: int = None, before: str = None, after: str = None):
        params = {
            'limit': limit,
            'offset': offset,
            'before': before,
            'after': after
        }
        params = {k: v for k, v in params.items() if v}

        r = requests.get(
            f"{self.endpoint}/{thread_id}/messages",
            headers=self._headers,
            params=params
        )

        return r.json()

    def get_last_message_from_user(self, msgs: List[dict], user: str) -> Any:
        msgs_sorted = sorted(
            msgs,
            key=lambda x: x['createdAt'],
            reverse=True
        )

        msgs_filtered = filter(
            lambda x: x['author']['login'] == user, msgs_sorted)
        msgs_filtered = list(msgs_filtered)

        msg = msgs_filtered[0]
        timestamp = msg['createdAt']

        return msg, timestamp

    def get_recent_threads(self, limit: int = 20) -> List[dict]:
        one_day_ago = datetime.now(pytz.utc) - timedelta(days=1)
        one_day_ago_str = one_day_ago.isoformat()

        threads = self.thread_list(limit=limit)
        recent_threads = [t for t in threads if t['lastMessage']
                          ['createdAt'] >= one_day_ago_str]
        return recent_threads


if __name__ == '__main__':
    import os
    import sys
    from datetime import datetime, timedelta
    import pytz

    sys.path.append(os.getcwd())

    from src.auth.OAuth import OAuth
    from dotenv import load_dotenv

    load_dotenv()
    oauth = OAuth(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET']
    )
    token = oauth.token[0]

    threads = Threads(access_token=token)

    recent_threads = threads.get_recent_threads()
    print(recent_threads)

    # threads_list = threads.thread_list
    # thread = threads.get(threads_list[0]['id'])

    # root = "adrianq123"
    # user = "bednarekparts"

    # msgs = threads.list_messages(threads_list[0]['id'])

    # root_last_msg = threads.get_last_message_from_user(msgs['messages'], root)
    # client_last_msg = threads.get_last_message_from_user(
    #     msgs['messages'], user)

    # to_answer = root_last_msg[1] < client_last_msg[1]

    # if to_answer:
    #     threads.send_message(
    #         threads_list[0]['id'], "Hej Mordeczko, jak tam? Nasz pracownik wkrótce się z Tobą skonktuje.")

    pass
