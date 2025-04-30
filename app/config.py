from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./travel_itinerary.db"
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Travel Itinerary API"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings() 