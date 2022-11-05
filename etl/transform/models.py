"""
The models containing Pydantic models designed for processing PostgreSQL
data on movies and subsequent loading to the Elasticsearch index 'movies'.
"""
from pydantic import BaseModel


class Person(BaseModel):
    """ A model for data about movie crews (directors, actors, writers). """
    id: str
    name: str
    role: str | None


class PersonWithFilms(Person):
    """ A model for data about person (directors, actors, writers). """
    film_ids: list[str] | None


class Genre(BaseModel):
    """ A model for data about genre films. """
    id: str
    name: str


class GenreWithDescription(Genre):
    """ A model for data about genre films with description. """
    id: str
    name: str
    description: str | None


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
    directors: list[Person] | None
    genre: list[Genre] | None
