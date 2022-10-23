import typing

from pydantic import parse_obj_as

from .models import Filmwork, Person


class Transform:

    def __init__(self, item):
        self.item = item

    def to_filmwork(self):
        people = parse_obj_as(typing.List[Person], self.item[0]['people'])
        film = parse_obj_as(typing.List[Filmwork], self.item)[0]

        film.actors = [p for p in people if p.role == 'actor']
        film.writers = [p for p in people if p.role == 'writer']

        film.director = ', '.join(sorted(p.name for p in people if p.role == 'director'))
        film.actors_names = ', '.join(sorted(p.name for p in film.actors))
        film.writers_names = ', '.join(sorted(p.name for p in film.writers))

        return film



