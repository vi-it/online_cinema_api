"""
This module tests API that handles film data.
"""

import http

import pytest

from tests.functional.models import Film
from tests.functional.settings import test_settings


@pytest.mark.asyncio
class TestFilmApi:
    """Test API that handles films data."""

    async def test_get_list(
        self,
        storages_clean,
        create_es_index,
        es_write_data,
        make_get_request,
        films_factory,
    ):
        """Test GET films list at /api/v1/films/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_movies)

        quantity = 3
        films = films_factory.create_batch(quantity)
        films_num = len(films)

        create_es_index(index_name=test_settings.es_index_movies)
        await es_write_data(
            [film.dict() for film in films],
            test_settings.es_index_movies,
            test_settings.es_id_field,
        )

        # Run #
        response = await make_get_request(url='films/')

        res = sorted([Film(**i) for i in response.body], key=lambda x: x.id)
        expected = sorted(films, key=lambda x: x.id)

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert films_num == quantity
        assert len(response.body) == films_num
        assert res == expected
