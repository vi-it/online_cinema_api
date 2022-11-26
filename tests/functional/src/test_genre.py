"""
This module tests API that handles genre data.
"""

import http

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

    @pytest.mark.parametrize('expected_answer',
                             [{'status': http.HTTPStatus.OK, 'length': 3}])
    async def test_cache_get_list(
            self,
            make_get_request,
            expected_answer,
    ):
        """Test caching for GET genres at /api/v1/genres/."""
        # Run #
        response = await make_get_request(url='genres/')

        # Assertions #
        assert response.status == expected_answer.get('status')
        assert len(response.body) == expected_answer.get('length')

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
