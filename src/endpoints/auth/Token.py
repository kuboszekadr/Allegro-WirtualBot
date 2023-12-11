import requests

from datetime import datetime
from typing import Optional

from src.models.Token import Token

class Token:
    endpoint = 'https://allegro.pl/auth/oauth/token'

    def __init__(self, client_id: str, client_secret: str, device_code: str):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.device_code: str = device_code 

        self.token: Optional(Token) = Token.load_from_file()

        if self.token is None:
            self.token = self.await_for_access_token(device_code)

    @property
    def token(self):
        ts = datetime.now().timestamp()
        
        if token.expiration_date <= ts:
            token = self.refresh(token.refresh_token)
        
        return token

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

        token = Token(**response)
        return token

    @cache
    def access_token(self, device_code: str) -> str:
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

        token = Token(**response)
        return token

    def await_for_access_token(self):
        while True:
            sleep(1)
            status_code, data = self.access_token(self.device_code)
            if status_code == 200:
                return data

    def cache(self, func):
        def wrapper(*args, **kwargs):
                token = func(*args, **kwargs)
                with open('./.token.json', 'w') as f:
                    f.writelines(token.model_dump_json(indent=4))
        return wrapper