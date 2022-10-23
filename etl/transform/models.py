from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str


class Filmwork(BaseModel):
    id: str
    imdb_rating: float
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[Person]
    writers: list[Person]
