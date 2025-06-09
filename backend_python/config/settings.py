import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field 

class Settings(BaseSettings):
    """
    Class for downloading configurations from .env
    """

    model_config = SettingsConfigDict(env_file = '.env', extra = 'ignore', case_sensitive=False)

    fastapi_api_key: str = Field(..., alias="FASTAPI_API_KEY")
    base_api_address: str = Field(..., alias="RENDER_EXTERNAL_HOSTNAME")


settings = Settings()