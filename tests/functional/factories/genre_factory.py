"""
This module is responsible for producing test genre data.
"""
import random

import factory

from .. import models


def get_name():
    """Return a random role person."""
    return random.choice(["Western", "Adventure", "Drama", "Romance"])


class GenresFactory(factory.Factory):
    class Meta:
        model = models.Genre

    id: str = factory.Faker('uuid4')
    name: str = factory.LazyFunction(get_name)
    description: str | None = factory.Faker('text')
