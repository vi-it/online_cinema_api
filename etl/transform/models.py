"""
The models containing Pydantic models designed for processing PostgreSQL
data on movies and subsequent loading to the Elasticsearch index 'movies'.
"""
import typing

from pydantic import BaseModel


class Person(BaseModel):
    """ A model for data about movie crews (directors, actors, writers). """
    id: str
    name: str
    role: str


class Filmwork(BaseModel):
    """
    A model for data about movies and data related to them.
    The model contains data necessary for loading to the Elatsticsearch
    index 'movies'.
    """
    id: str
    title: str
    description: str | None
    imdb_rating: float | None
    director: list[str] | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    actors: list[Person] | None
    writers: list[Person] | None
    genre: list[str] | None

