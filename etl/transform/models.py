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
    description: typing.Optional[str]
    imdb_rating: typing.Optional[float]
    director: typing.Optional[list[str]]
    actors_names: typing.Optional[list[str]]
    writers_names: typing.Optional[list[str]]
    actors: typing.Optional[list[Person]]
    writers: typing.Optional[list[Person]]
    genre: typing.Optional[list[str]]

