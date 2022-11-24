from pydantic import BaseModel, Field

from .base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    name: str
    role: str | None
    film_ids: list[str] | list

