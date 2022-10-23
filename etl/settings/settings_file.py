from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    AmqpDsn,
    Field,
)
import pydantic

import os
from dotenv import load_dotenv
load_dotenv()

class PGSettings(BaseSettings):
    """PostgreSQL settings."""
    host: str
    dbname: str
    password: str
    port: str
    user: str
    options: str = '-c search_path=content'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
