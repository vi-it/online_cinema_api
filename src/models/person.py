from pydantic import BaseModel, Field

from src.models.base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    full_name: str = Field(alias='name')
    role: str | None
    film_ids: list[str | None]

