import typing

from src.models.base import BaseOrjsonModel


class ID(BaseOrjsonModel):
    id: str
    name: str


class Film(BaseOrjsonModel):
    id: str
    title: str
    description: str | None
    creation_date: str | None
    imdb_rating: float | None
    type: str | None
    genre: typing.List[ID] | None
    actors: typing.List[ID] | None
    directors: typing.List[ID] | None
    writers: typing.List[ID] | None
    actors_names: typing.List[str] | None
    director: typing.List[str] | None
    writers_names: typing.List[str] | None

