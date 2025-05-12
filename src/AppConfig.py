from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    
    client_id: str
    client_secret: str
    user_name: str
    api_base_url: str
    auth_base_url: str
    device_code_url: str

    class Config:
        env_prefix = 'ALLEGRO_'

config = AppConfig()