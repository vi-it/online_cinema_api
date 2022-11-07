import typing

import orjson
from pydantic import BaseModel, Field

from src.models import utility


class ID(BaseModel):
    id: str
    name: str


class Film(BaseModel):
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

    class Config:
        """Заменяем стандартную работу с json на более быструю."""
        alias = 'movies'
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps
