from pydantic import BaseModel, Field
from typing import List, Optional

class AccessToken (BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: Optional(int)
    scope: List [str] = Field(min_items=1)
    allegro_api: bool
    iss: str
    jti: str
    expiration_date: int

    def __post_init__(self):
        if self.expiration_date is None:    
            self.expiration_date = int(datetime.datetime.now().timestamp()) + self.expires_in

    @classmethod
    def load_from_file(cls):
        if not os.path.exists('./.token.json'):
            return None

        with open('./.token.json', 'r') as f:
            data = json.load(f)
            result = Token(**data)
            return result

    # def cache(self, func):
    #     def wrapper(*args, **kwargs):
    #         token = func(*args, **kwargs) 
    #         with open('./.token.json', 'w') as f:
    #             json.dump(self.dict(), f)
    #         return token
