import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(PROJECT_ROOT, '.env'),
        extra='ignore',
        case_sensitive=False
    )

    fastapi_api_key: str = Field(..., alias="FASTAPI_API_KEY")
    base_api_address: str = Field(..., alias="RENDER_EXTERNAL_HOSTNAME")
    database_url: str = Field(..., alias="DATABASE_URL")
    
settings = Settings()