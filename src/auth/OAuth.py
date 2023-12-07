import requests
import json
import os
import datetime

from time import sleep

from requests.auth import HTTPBasicAuth


class OAuth:
    endpoint = 'https://allegro.pl/auth/oauth'

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def token(self):
        ts = datetime.datetime.now().timestamp()

        if os.path.exists('./.token.json'):
            with open('./.token.json', 'r') as f:
                result = json.load(f)

            if result['expiration_date'] <= ts:
                result = self.get_next_token(result['refresh_token'])
        else:
            data = self.device_code
            token_data = self.await_for_access_token(
                data['interval'], data['device_code'])
            token_data = token_data.json()

            with open('./.token.json', 'w') as f:
                token_data['expiration_date'] = int(
                    datetime.datetime.now().timestamp()) + token_data['expires_in']
                json.dump(token_data, f)

        return result['access_token'], result['refresh_token']

    def access_token(self, device_code: str) -> str:
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code
        }

        response = requests.post(
            f"{self.endpoint}/token",
            auth=(self.client_id, self.client_secret),
            headers=headers,
            data=data,
            verify=False)

        return response.status_code, response

    def await_for_access_token(self, inteval: int, device_code: str):
        while True:
            sleep(inteval)
            status_code, data = self.access_token(device_code)
            if status_code == 200:
                return data

    def get_next_token(self, refresh_token: str) -> str:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        access_token_response = requests.post(
            f'{self.endpoint}/token',
            data=data,
            verify=False,
            allow_redirects=False,
            auth=(self.client_id, self.client_secret)
        )

        token_data = access_token_response.json()
        access_token = token_data['access_token']

        with open('./.token.json', 'w') as f:
            token_data['expiration_date'] = int(
                datetime.datetime.now().timestamp()) + token_data['expires_in']
            json.dump(token_data, f)
        return access_token, token_data['refresh_token']

    @property
    def device_code(self):
        payload = {'client_id': self.client_id}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        r = requests.post(
            url=f"{self.endpoint}/device",
            auth=(self.client_id, self.client_secret),
            headers=headers,
            data=payload,
            verify=False
        )
        return r.json()


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    oauth = OAuth(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET']
    )

    print(oauth.token)
