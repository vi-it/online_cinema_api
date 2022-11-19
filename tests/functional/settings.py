"""
This module is responsible for storing functional tests' settings.
"""

from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    """A storage class for functional tests' settings."""
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_port: str = Field('9200', env='ELASTIC_PORT')
    es_index: str = ...
    es_id_field: str = ...
    es_index_mapping: dict = ...

    redis_host: str = ...
    service_url: str = ...


test_settings = TestSettings()
