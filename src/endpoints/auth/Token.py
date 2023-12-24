import requests
import logging 

from datetime import datetime
from typing import Optional
from time import sleep

if __name__ == '__main__':
    import sys
    import os

    sys.path.append(os.getcwd())

from src.models.AccessToken import AccessToken

logging.basicConfig(level=logging.INFO)

class Token:
    endpoint = 'https://allegro.pl.allegrosandbox.pl/auth/oauth/token'

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            device_code: str = None,
    ):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.access_token: Optional(AccessToken) = AccessToken.load_from_file()

        if self.access_token is None:
            self.init_access_token()

    @property
    def value(self) -> str:
        ts = datetime.now().timestamp()

        if self.access_token.expiration_date <= ts:
            self.access_token = self.get_access_token()

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
    def get_access_token(self) -> str:
        logging.info('Refreshing token...')
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.access_token.refresh_token
        }

        try:
            response = requests.post(
                url=self.endpoint,
                data=data,
                verify=False,
                allow_redirects=False,
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
            self.access_token = AccessToken.model_validate(response.json())
            return self.access_token

        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')  # Specific HTTP error
        except Exception as err:
            logging.error(f'An error occurred: {err}')  # Other errors
        return None
    
    
    def get_device_code(self):
        # source: https://developer.allegro.pl/tutorials/uwierzytelnianie-i-autoryzacja-zlq9e75GdIR#python
        payload = {'client_id': self.client_id}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(
                "https://allegro.pl.allegrosandbox.pl/auth/oauth/device",
                auth=(self.client_id, self.client_secret),
                headers=headers,
                data=payload,
                verify=False
            )
            response.raise_for_status()
            result = response.json()
            logging.warning(f"Go to: {result['verification_uri_complete']}")
            self.device_code = result['device_code']
            return result
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')  # Specific HTTP error
        except Exception as err:
            logging.error(f'An error occurred: {err}')  # Other errors
        return None      

    def await_for_user_approval(self):
        self.get_device_code()
        while True:
            sleep(30)
            token = self.first_time_access_token()
            if token is not None:
                return token

    def first_time_access_token(self):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': self.device_code
        }

        try:
            response = requests.post(
                url=self.endpoint,
                auth=(self.client_id, self.client_secret),
                headers=headers,
                data=data,
                verify=False
            )
            response.raise_for_status()
            self.access_token = AccessToken.model_validate(response.json())
            return self.access_token

        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.error(f'An error occurred: {err}')
        return None
    
    def init_access_token(self):
        self.get_device_code
        self.await_for_user_approval()
        self.get_access_token()
        


if __name__ == '__main__':
    from src.AppConfig import config
    token = Token(
        client_id=config.allegro.client_id,
        client_secret=config.allegro.client_secret,
    )

    print(token.value)
