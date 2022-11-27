"""
This module tests API that handles genre data.
"""

import http
import json

import pytest

from tests.functional.settings import test_settings
from tests.functional.models import Genre


@pytest.mark.asyncio
class TestGenreApi:
    """Test API that handles genres data."""

    async def test_get_list(
            self,
            storages_clean,
            create_es_index,
            es_write_data,
            make_get_request,
            genres_factory
    ):
        """ Test GET genres list at /api/v1/genres/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_genres)

        quantity = 3
        genres = genres_factory.create_batch(quantity)
        genres_num = len(genres)

        create_es_index(index_name=test_settings.es_index_genres)
        await es_write_data(
            [genre.dict() for genre in genres],
            test_settings.es_index_genres,
            test_settings.es_id_field,
        )

        # Run #
        response = await make_get_request(url='genres/')

        res = sorted([Genre(**i) for i in response.body], key=lambda x: x.id)
        expected = sorted(genres, key=lambda x: x.id)

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert genres_num == quantity
        assert len(response.body) == genres_num
        assert res == expected

    async def test_get_by_id(
            self,
            create_es_index,
            es_write_data,
            make_get_request,
            genres_factory,
    ):
        """ Test GET genre by id at /api/v1/genres/{genre_id}."""
        # Setup #
        es_data = [genres_factory().dict() for _ in range(5)]
        create_es_index(index_name=test_settings.es_index_genres)
        await es_write_data(es_data, test_settings.es_index_genres,
                            test_settings.es_id_field)
        genre = Genre(**es_data[0])

        # Run #
        response = await make_get_request(url=f'genres/{genre.id}')

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert Genre(**response.body) == genre.dict()

    async def test_get_by_id_cached(
             self,
             storages_clean,
             create_es_index,
             es_write_data,
             make_get_request,
             genres_factory,
             redis_client,
    ):
        """Test caching for GET genres at /api/v1/genres/{genre_id}."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_genres)

        genres = genres_factory.create_batch(2)
        target_genre = genres[0]

        create_es_index(index_name=test_settings.es_index_genres)
        await es_write_data(
            [genre.dict() for genre in genres],
            test_settings.es_index_genres,
            test_settings.es_id_field,
        )

        await make_get_request(url=f'genres/{target_genre.id}')

        # Run #
        cached = await redis_client.get(target_genre.id)

        # Assertions #
        assert Genre(**json.loads(cached.decode('utf-8'))) == target_genre

    async def test_not_found(
            self,
            make_get_request,
    ):
        """
        Test the response status when genre is not found by id at
        /api/v1/genres/{genre_id}.
        """
        # Run #
        response = await make_get_request(url=f'genres/test-uid')

        # Assertions #
        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Genre with id test-uid not found'}
