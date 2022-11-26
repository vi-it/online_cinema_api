"""
This module is responsible for storing functional tests' settings.
"""

from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    """A storage class for functional tests' settings."""
    es_host: str = Field('elastic', env='ELASTIC_HOST')
    es_port: str = Field('9200', env='ELASTIC_PORT')
    es_index: str = 'movies'
    es_index_genres: str = Field('genres')
    es_index_movies: str = Field('movies')
    es_index_persons: str = Field('persons')
    es_id_field: str = 'id'

    redis_host: str = Field('redis', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')
    redis_connection_timeout = Field(60, env='REDIS_CONNECTION_TIMEOUT')

    service_host: str = Field('app', env='PROJECT_HOST')
    service_port: str = Field('8000', env='PROJECT_PORT')


test_settings = TestSettings()
