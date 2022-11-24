"""
This module is responsible for producing test film data.
"""

import factory

from .. import models


class FilmFactory(factory.Factory):
    class Meta:
        model = models.Film

    id: str = factory.Faker('uuid4')
    title: str = factory.Faker('name')
    imdb_rating: float | None = factory.Faker('pyfloat', positive=True)
