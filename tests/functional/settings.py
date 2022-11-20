"""
This module is responsible for storing functional tests' settings.
"""

from pydantic import BaseSettings, Field


# TODO: класс недописан
class TestSettings(BaseSettings):
    """A storage class for functional tests' settings."""
    es_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    es_port: str = Field('9200', env='ELASTIC_PORT')
    # es_index: str = 'movies'
    # es_id_field: str = '3'
    # es_index_mapping: dict = ...

    redis_host: str = Field('127.0.0.1:6380', env='ELASTIC_HOST')
    service_url: str = 'http://127.0.0.1/'

test_settings = TestSettings()
