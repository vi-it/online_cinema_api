"""
This module is responsible for producing test film data.
"""

import factory

from .. import models


class FilmsFactory(factory.Factory):
    class Meta:
        model = models.Film

    id: str = factory.Faker('uuid4')
    title: str = factory.Faker('name')
    # description: str | None
    # creation_date: str | None
    imdb_rating: float | None = factory.Faker('pyfloat', positive=True)
    # type: # str | None = factory.Faker('')
    # genre: list[models.ID] | None
    # actors: list[ID] | None
    # directors: list[ID] | None
    # writers: list[ID] | None
    # actors_names: list[str] | None
    # director: list[str] | None
    # writers_names: list[str] | None
