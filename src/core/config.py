import os
import typing
from logging import config as logging_config

from src import models
from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILM_CACHE_EXPIRE_IN_SECONDS = 10 * 5
GENRE_CACHE_EXPIRE_IN_SECONDS = 10 * 5
PERSON_CACHE_EXPIRE_IN_SECONDS = 10 * 5
CACHE_EXPIRE_IN_SECONDS = 2 * 5

ES_INDEXES = {
    'film': ('movies', 'Film'),
    'genre': ('genres', 'Genre'),
    'person': ('persons', 'Person')
}

ES_INDEX_GENRES = 'genres'
ES_INDEX_PERSONS = 'persons'
ES_INDEX_MOVIES = 'movies'

ES_SIZE = 1000

CINEMA_MODEL = typing.TypeVar('CINEMA_MODEL',
                              models.Film,
                              models.Person,
                              models.Genre)
