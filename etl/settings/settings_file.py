"""
The module contains Pydantic models for environment variables
"""
import pydantic

import os
from dotenv import load_dotenv


load_dotenv()


class PGSettings(pydantic.BaseSettings):
    """PostgreSQL settings."""
    host: str = os.environ.get('host')
    dbname: str = os.environ.get('movies_database')
    password: str = os.environ.get('password')
    port: str = os.environ.get('port')
    user: str = 'app'
    options: str = '-c search_path=content'


class ESTSettings(pydantic.BaseSettings):
    """Elasticsearc settings."""
    es_host: str = os.environ.get('ES_HOST')
    es_port: str = os.environ.get('ES_PORT')


PG = PGSettings().dict()
EST = ESTSettings().dict()
