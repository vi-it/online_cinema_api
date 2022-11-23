from .base import BaseOrjsonModel


class ID(BaseOrjsonModel):
    id: str
    name: str


class Film(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float | None
