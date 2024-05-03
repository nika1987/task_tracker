"""This file contains constants to configure the application"""
from pydantic_settings import BaseSettings
# --------------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()
ENV_FILE = '../.env'


class Settings(BaseSettings):
    """This class serves to get settings from the environment variables"""
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ENV_FILE


sets = Settings()

README_FILE = '../README.md'

DB_URI = (f'postgresql+asyncpg://{sets.POSTGRES_USER}:{sets.POSTGRES_PASSWORD}'
          f'@{sets.POSTGRES_HOST}:{sets.POSTGRES_PORT}/{sets.POSTGRES_DB}')
