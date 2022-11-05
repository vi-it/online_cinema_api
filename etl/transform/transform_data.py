import typing

from pydantic import parse_obj_as

from .models import (Filmwork, GenreWithDescription, Person,
                     PersonWithFilms)


class Transform:
    """
    A class for transforming PostgreSQL movies data to a format
    suitable for loading to the Elasticsearch index 'movies'.
    """

    def __init__(self, index) -> None:
        self.index = index

    def transform(self, item):
        if self.index == 'movies':
            return self.to_filmwork(item)
        elif self.index == 'persons':
            return self.to_person(item)
        return self.to_genre(item)

    @staticmethod
    def to_filmwork(item) -> Filmwork:
        """Transform data in accordance with the Pydantic models."""
        people = parse_obj_as(typing.List[Person],
                              item[0]['people'])
        film = parse_obj_as(typing.List[Filmwork], item)[0]

        actors_ = [p for p in people if p.role == 'actor']
        writers_ = [p for p in people if p.role == 'writer']
        directors_ = [p for p in people if p.role == 'director']

        film.actors = [{'id': p.id, 'name': p.name} for p in actors_]
        film.writers = [{'id': p.id, 'name': p.name} for p in writers_]
        film.directors = [{'id': p.id, 'name': p.name} for p in directors_]

        film.genre = [{'id': g.id, 'name': g.name} for g in film.genre]

        film.director = sorted(p.name for p in people if p.role == 'director')
        film.actors_names = sorted(p.name for p in actors_)
        film.writers_names = sorted(p.name for p in writers_)
        return film

    @staticmethod
    def to_genre(item) -> GenreWithDescription:
        genre = parse_obj_as(GenreWithDescription, item[0])
        return genre

    @staticmethod
    def to_person(item) -> PersonWithFilms:
        person = parse_obj_as(PersonWithFilms, item[0])
        return person
