if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.getcwd())

    from dotenv import load_dotenv
    load_dotenv()

import requests
import logging
import os
import pytz

from datetime import datetime, timedelta
from typing import List

from src.endpoints.auth.Token import Token
from src.endpoints.messaging.Thread import Thread
from src.models.Thread import MessageThread

class Threads:
    endpoint = 'https://api.allegro.pl/messaging/threads'

    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.threads: List[Thread] = None

    def _headers(self):
        headers = {
            'Authorization': f'Bearer {self.token.value}',
            'Accept': 'application/vnd.allegro.public.v1+json',
            'Content-Type': 'application/vnd.allegro.public.v1+json'
        }
        return headers

    def get(
            self, 
            limit: int = 20,
            cutoff: int = None
            ) -> List[Thread]:
        
        r = requests.get(
            self.endpoint,
            headers=self._headers(),
            params={'limit': limit}
        )

        if not r.ok:
            logging.error(
                f"Failed to retrieve data. Status Code: {r.status_code}")
            #TODO: Handle this error
            return None

        threads_raw = r.json()['threads']
        results = [MessageThread(**t) for t in threads_raw]

        if cutoff is not None:
            cutoff = datetime.now(pytz.utc) - timedelta(days=cutoff)
            cutoff_str = cutoff.isoformat()        

            results = filter(
                lambda x: x.lastMessageDateTime >= cutoff_str,
                results
            )
            results = list(results)

        self.threads = [Thread(t.id, self.token) for t in results]
        return self.threads

if __name__ == '__main__':
    from src.AppConfig import config
    token = Token(
        client_id=config.allegro.client_id,
        client_secret=config.allegro.client_secret,
        device_code=config.allegro.device_code
    )

    threads = Threads(token)
    threads.get()

    root = "adrianq123"

    thread = threads.threads[0]
    thread.get_messages()
    print(thread.get_last_message_from_user(root))
    
