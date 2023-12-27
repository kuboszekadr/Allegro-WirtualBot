import requests
import logging 

from datetime import datetime
from typing import Optional
from time import sleep

if __name__ == '__main__':
    import sys
    import os

    sys.path.append(os.getcwd())

from src.AppConfig import config
from src.models.AccessToken import AccessToken

logging.basicConfig(level=logging.INFO)

class Token:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            device_code: Optional[str] = None,
    ):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.device_code: str = device_code

        self.access_token: Optional(AccessToken) = AccessToken.load_from_file()

        if self.access_token is None:
            self.init_device()

    @property
    def endpoint(self) -> str:
        result = f'https://allegro.pl{config.allegro.prefix}/auth/oauth/token'
        return result


    @property
    def value(self) -> str:
        ts = datetime.now().timestamp()

        if self.access_token.expiration_date <= ts:
            self.access_token = self.refresh(self.access_token.refresh_token)

        result = self.access_token.access_token
        return result

    @staticmethod
    def cache(func):
        def wrapper(*args, **kwargs):
            token = func(*args, **kwargs)
            if token is None:
                return None

            with open('./.token.json', 'w') as f:
                f.writelines(token.model_dump_json(indent=4))
            return token
        return wrapper

    @cache
    def refresh(self, refresh_token: str) -> str:
        logging.info('Refreshing token...')
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = requests.post(
            url=self.endpoint,
            data=data,
            verify=False,
            allow_redirects=False,
            auth=(self.client_id, self.client_secret)
        )

        data = response.json()
        self.access_token = AccessToken.model_validate(data)
        return self.access_token

    @cache
    def get_access_token(self) -> str:
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': self.device_code
        }

        response = requests.post(
            url=self.endpoint,
            auth=(self.client_id, self.client_secret),
            headers=headers,
            data=data,
            verify=False
        )

        result = None
        if response.ok:
            self.access_token = AccessToken.model_validate(response.json())
            result = self.access_token
        else:
            logging.warning(response.json())
        return result

    def get_device_code(self):
        # source: https://developer.allegro.pl/tutorials/uwierzytelnianie-i-autoryzacja-zlq9e75GdIR#python
        payload = {'client_id': self.client_id}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        response = requests.post(
            f"https://allegro.pl{config.allegro.prefix}/auth/oauth/device",
            auth=(self.client_id, self.client_secret),
            headers=headers,
            data=payload,
            verify=False
        )

        result = response.json()
        self.device_code = result['device_code']

        return result

    def await_access_token(self):
        while True:
            sleep(5)
            token = self.get_access_token()

            if token is not None:
                return token

    def init_device(self):
        device_code = self.get_device_code()
        logging.warn(f"Go to: {device_code['verification_uri_complete']}")
        self.await_access_token()


if __name__ == '__main__':
    from src.AppConfig import config
    token = Token(
        client_id=config.allegro.client_id,
        client_secret=config.allegro.client_secret,
        device_code=config.allegro.device_code
    )

    print(token.value)