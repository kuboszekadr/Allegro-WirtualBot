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
from src.models.Dispute import Dispute

class Disputes:
    endpoint = 'https://api.allegro.pl.allegrosandbox.pl/sale/disputes'

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

    def get(
            self, 
            limit: int = 20,
            cutoff: int = None
            ) -> List[Dispute]:
        
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

        disputes_raw = r.json()['disputes']
        results = [Dispute(**d) for d in disputes_raw]

        if cutoff is not None:
            cutoff = datetime.now(pytz.utc) - timedelta(days=cutoff)
            cutoff_str = cutoff.isoformat()        

            results = filter(
                lambda x: x.updatedAt >= cutoff_str,
                results
            )
            results = list(results)

        self.disputes = results
        return self.disputes

if __name__ == '__main__':
    from src.AppConfig import config
    token = Token(
        client_id=config.allegro.client_id,
        client_secret=config.allegro.client_secret,
    )

    disputes = Disputes(token)
    disputes.get()

    for dispute in disputes.disputes:
        print(dispute)