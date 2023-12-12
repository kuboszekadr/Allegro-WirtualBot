import requests

from datetime import datetime
from typing import Optional
from time import sleep

if __name__ == '__main__':
    import sys
    import os

    sys.path.append(os.getcwd())

from src.models.AccessToken import AccessToken

class Token:
    endpoint = 'https://allegro.pl/auth/oauth/token'

    def __init__(
            self, 
            device_code: Optional[str] = None,
            client_id: Optional[str] = None, 
            client_secret: Optional[str] = None, 
            ):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.device_code: str = device_code 

        self.access_token: Optional(AccessToken) = AccessToken.load_from_file()

        if device_code is None and client_id is None and client_secret is None:
            # TODO: Handle this error
            raise Exception('Missing required arguments.')

        if self.access_token is None:
            self.access_token = self.await_for_access_token(device_code)

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
                with open('./.token.json', 'w') as f:
                    f.writelines(token.model_dump_json(indent=4))
        return wrapper

    @cache
    def refresh(self, refresh_token: str) -> str:
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
        token = AccessToken.model_validate(data)
        return token

    @cache
    def get_access_token(self, device_code: str) -> str:
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code
        }

        response = requests.post(
            url=self.endpoint,
            auth=(self.client_id, self.client_secret),
            headers=headers,
            data=data,
            verify=False
            )

        token = AccessToken(**response)
        return token

    def await_for_access_token(self):
        while True:
            sleep(1)
            status_code, data = self.get_access_token(self.device_code)
            if status_code == 200:
                return data


if __name__ == '__main__':
    from src.AppConfig import config
    token = Token(
        client_id=config.allegro.client_id,
        client_secret=config.allegro.client_secret,
        device_code=config.allegro.device_code
    )

    print(token.value)