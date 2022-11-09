from pydantic import BaseModel

import orjson
from src.models import utility


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps
