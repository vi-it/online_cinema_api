import os
import typing
from logging import config as logging_config

from pydantic import BaseSettings, Field

from src import models
from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """The class contains settings for the project."""
    BASE_DIR = Field(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    DEBUG: str = Field('False', env='DEBUG')

    ELASTIC_HOST: str = Field('127.0.0.1', env='ELASTIC_HOST')
    ELASTIC_PORT: int = Field(9200, env='ELASTIC_PORT')

    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: int = Field(6379, env='REDIS_PORT')

    PROJECT_NAME = Field('movies', env='PROJECT_NAME')

    ES_INDEX_GENRES: str = Field('genres')
    ES_INDEX_MOVIES: str = Field('movies')
    ES_INDEX_PERSONS: str = Field('persons')

    ES_SIZE: int = Field(1000)

    CACHE_EXPIRE_IN_SECONDS: int = Field(2 * 5)
    FILM_CACHE_EXPIRE_IN_SECONDS: int = Field(10 * 5)
    GENRE_CACHE_EXPIRE_IN_SECONDS: int = Field(10 * 5)
    PERSON_CACHE_EXPIRE_IN_SECONDS: int = Field(10 * 5)

    CINEMA_MODEL = typing.TypeVar('CINEMA_MODEL',
                                  models.Film,
                                  models.Person,
                                  models.Genre)


settings = Settings()
