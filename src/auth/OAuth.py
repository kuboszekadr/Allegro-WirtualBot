import requests
import json
import os

from time import sleep

from requests.auth import HTTPBasicAuth

class OAuth:
    endpoint = 'https://allegro.pl/auth/oauth'

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

        self._auth = HTTPBasicAuth(self.client_id, self.client_secret)
    
    @property
    def token(self):

        if os.path.exists('./.token.json'):
            with open('./.token.json', 'r') as f:
                result = json.load(f)
        else:
            data = self.device_code
            token_data = oauth.await_for_access_token(data['interval'], data['device_code'])
        
            with open('./.token.json', 'w') as f:
                json.dump(token_data.json(), f)
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

    # def refresh_token(self, authorization_code: str) -> str:
    #     data = {
    #         'grant_type': 'authorization_code', 
    #         'code': authorization_code
    #         }
    #     access_token_response = requests.post(
    #         f'{self.endpoint}/token', 
    #         data=data, 
    #         verify=False,
    #         allow_redirects=False, 
    #         auth=(self.client_id, self.client_secret)
    #         )
        
    #     tokens = json.loads(access_token_response.text)
    #     access_token = tokens['refresh_token']
    #     return access_token
    
    # def get_next_token(self, refresh_token: str) -> str:
    #     data = {
    #         'grant_type': 'refresh_token', 
    #         'refresh_token': refresh_token
    #         }
        
    #     access_token_response = requests.post(
    #         f'{self.endpoint}/token', 
    #         data=data, 
    #         verify=False,
    #         allow_redirects=False, 
    #         auth=(self.client_id, self.client_secret)
    #         )
        
    #     tokens = json.loads(access_token_response.text)
    #     access_token = tokens['access_token']
    #     return access_token        
    
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
    oauth = OAuth("d1c1a54a29484034928ee75c23b2dba8", "C5HPyjipUvEzfHoC9zTidXwoTtGA6azasFgp9rhW32xPbkMdfq4pnIlNTjyoph9n")
    
    code = oauth.device_code
    oauth.await_for_access_token(code['interval'], code)