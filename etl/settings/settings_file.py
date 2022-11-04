"""
The module contains Pydantic models for environment variables
"""
import pydantic

import os
from dotenv import load_dotenv

load_dotenv()


class PGSettings(pydantic.BaseSettings):
    """PostgreSQL settings."""
    host: str = os.environ.get('POSTGRES_DB_HOST')
    dbname: str = os.environ.get('POSTGRES_DB')
    password: str = os.environ.get('POSTGRES_PASSWORD')
    port: str = os.environ.get('POSTGRES_DB_PORT')
    user: str = os.environ.get('POSTGRES_USER')
    options: str = '-c search_path=content'


class ESTSettings(pydantic.BaseSettings):
    """Elasticsearc settings."""
    es_host: str = os.environ.get('ES_HOST')
    es_port: str = os.environ.get('ES_PORT')
    es_indexes: list[str] = ['movies', 'persons', 'genres']


PG = PGSettings(
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD')
).dict()
EST = ESTSettings().dict()