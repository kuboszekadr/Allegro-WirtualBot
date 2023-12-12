import json
import os

from pydantic import BaseModel, Field
from typing import List, Optional

from datetime import datetime as dt

class AccessToken (BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: str = Field(min_items=1)
    allegro_api: bool
    iss: str
    jti: str
    expiration_date: Optional[int]

    def model_post_init(self, *args, **kwargs):
        if self.expiration_date is None:    
            self.expiration_date = int(dt.now().timestamp()) + self.expires_in

    @classmethod
    def load_from_file(cls):
        if not os.path.exists('./.token.json'):
            return None

        with open('./.token.json', 'r') as f:
            data = json.load(f)
            result = AccessToken.model_validate(data)
            return result

