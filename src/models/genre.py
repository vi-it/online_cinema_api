import orjson
from pydantic import BaseModel

from src.models import utility


class Genre(BaseModel):
    id: str
    name: str
    description: str | None

    class Config:
        """Заменяем стандартную работу с json на более быструю."""
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps
