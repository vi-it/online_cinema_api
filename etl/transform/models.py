import typing

from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str
    role: str


class Filmwork(BaseModel):
    id: str
    title: str
    description: typing.Optional[str]
    imdb_rating: typing.Optional[float]
    type: str
    director: typing.Optional[list[str]]
    actors_names: typing.Optional[list[str]]
    writers_names: typing.Optional[list[str]]
    actors: typing.Optional[list[Person]]
    writers: typing.Optional[list[Person]]
    genre: typing.Optional[list[str]]


