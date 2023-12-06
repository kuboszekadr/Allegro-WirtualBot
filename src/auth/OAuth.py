import requests
from requests.auth import HTTPBasicAuth


class OAuth:
    endpoint = 'https://allegro.pl/auth/oauth'

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self._auth = HTTPBasicAuth(self.client_id, self.client_secret)

    @property
    def token(self) -> str:
        payload = {'grant_type': 'client_credentials'}

        response = requests.post(
            url=f'{self.endpoint}/token',
            auth=self._auth,
            data=payload
        )

        if not response.ok:
            print(f"Failed to retrieve the access token. Status Code: {response.status_code}")
            return None
        
        results = response.json()['access_token']
        return results
    
    def refresh_token(self) -> str:
        raise NotImplementedError()
    
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
        return r
