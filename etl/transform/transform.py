import datetime
import typing

from pydantic import parse_obj_as

from models import Filmwork, Person


def to_filmwork(item):
    item = [{'id': '3bdae84f-9a04-4b04-9f7c-c05582d529e5', 'type': 'movie', 'genre': ['Action', 'Sci-Fi'], 'title': 'Star Wars: Qui-Gon Jinn III', 'people': [{'id': '06c281cf-c2be-46b7-930c-8f4975f07b02', 'name': 'David Anghel', 'role': 'actor'}, {'id': '06c281cf-c2be-46b7-930c-8f4975f07b02', 'name': 'David Anghel', 'role': 'director'}, {'id': '06c281cf-c2be-46b7-930c-8f4975f07b02', 'name': 'David Anghel', 'role': 'writer'}, {'id': '08524e56-38a3-411a-8c30-dfca9b54aca0', 'name': 'Pauli Janhunen Calderón', 'role': 'actor'}, {'id': '08524e56-38a3-411a-8c30-dfca9b54aca0', 'name': 'Pauli Janhunen Calderón', 'role': 'director'}, {'id': 'b35228ed-88b4-4f64-90c4-00d4953c053b', 'name': 'Emilio Janhunen Calderón', 'role': 'actor'}, {'id': 'e84b46b0-1623-41d1-8ab8-26db182d1261', 'name': 'Marina Janhunen Calderón', 'role': 'actor'}], 'created': '2022-10-17T03:37:41.228911+00:00', 'modified': '2022-10-17T03:37:41.228911+00:00', 'description': "The Jedi temple gets attacked by an army of Siths. It's up to Qui-Gon Jinn and Obi-Wan Kenobi to stop the invasion. Meanwhile Darth Sidious seeks after a new apprentice.", 'imdb_rating': 7.2}]

    people = parse_obj_as(typing.List[Person], item[0]['people'])
    film = parse_obj_as(typing.List[Filmwork], item)[0]
    film.director = [p for p in people if p.role == 'director']
    film.actors = [p for p in people if p.role == 'actor']
    film.writers = [p for p in people if p.role == 'writer']
    film.actors_names = [p.name for p in film.actors]
    film.writers_names = [p.name for p in film.writers]


to_filmwork(1)
