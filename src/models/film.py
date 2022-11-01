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
    director: str | None
    actors_name: str | None
    writers_name: str | None
    actors: str | None
    writers: str | None
    genre: str | None

    class Config:
        """Заменяем стандартную работу с json на более быструю."""
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps
