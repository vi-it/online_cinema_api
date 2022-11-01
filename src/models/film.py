import typing

import orjson
from pydantic import BaseModel

from src.models import utility


class Film(BaseModel):
    id: str
    title: str
    description: str | None
    creation_date: str | None
    idmb_rating: float | None
    type: str | None
    genre: typing.List[str]
    actors: typing.List[str] | None
    directors: typing.List[str] | None
    writers: typing.List[str] | None
    actors_names: typing.List[str] | None
    directors_names: typing.List[str] | None
    writers_names: typing.List[str] | None

    class Config:
        """Заменяем стандартную работу с json на более быструю."""
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps
