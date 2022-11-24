"""
This module is responsible for producing test person data.
"""
import random
import uuid

import factory

from .. import models
from . import FilmsFactory


def get_role():
    "Return a random role person."
    return random.choice(['actor', 'writer', 'director'])


def get_films_uid():
    "Return uids."
    return [str(uuid.uuid4()) for i in range(random.randint(1,4))] # todo: исправить после реализации factory films


class PersonsFactory(factory.Factory):
    class Meta:
        model = models.Person

    id: str = factory.Faker('uuid4')
    name: str = factory.Faker('name')
    role: str | None = factory.LazyFunction(get_role)
    film_ids: list[str] | list = factory.LazyFunction(get_films_uid)
