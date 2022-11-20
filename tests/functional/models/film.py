from .base import BaseOrjsonModel


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
    genre: list[ID] | None
    actors: list[ID] | None
    directors: list[ID] | None
    writers: list[ID] | None
    actors_names: list[str] | None
    director: list[str] | None
    writers_names: list[str] | None
