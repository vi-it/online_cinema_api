import orjson
from pydantic import BaseModel

from src.models import utility


class Person(BaseModel):
    id: str
    full_name: str
    role: str | None
    film_ids: list[str | None]

    class Config:
        """Заменяем стандартную работу с json на более быструю."""
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps
