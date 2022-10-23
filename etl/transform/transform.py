import typing

from pydantic import parse_obj_as

from .models import Filmwork, Person


class Transform:

    def __init__(self, item):
        self.item = item

    def to_filmwork(self):
        people = parse_obj_as(typing.List[Person], self.item[0]['people'])
        film = parse_obj_as(typing.List[Filmwork], self.item)[0]

        actors_ = [p for p in people if p.role == 'actor']
        writers_ = [p for p in people if p.role == 'writer']

        film.actors = [{'id': p.id, 'name': p.name} for p in actors_]
        film.writers = [{'id': p.id, 'name': p.name} for p in writers_]

        film.director = sorted(p.name for p in people if p.role == 'director')
        film.actors_names = sorted(p.name for p in actors_)
        film.writers_names = sorted(p.name for p in writers_)

        return film



