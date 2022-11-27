"""
This module tests API that handles film data.
"""

import http
import json

import pytest
from tests.functional.models import Film
from tests.functional.settings import test_settings


@pytest.mark.asyncio
class TestFilmApi:
    """Test API that handles films data."""

    async def test_get_list(
            self,
            storages_clean,
            upload_data_to_es_index,
            make_get_request,
            films_factory,
    ):
        """Test GET films list at /api/v1/films/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_movies)

        quantity = 3
        films = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=films_factory,
            index_name=test_settings.es_index_movies,
            es_id_field=test_settings.es_id_field
        ).__anext__()

        # Run #
        response = await make_get_request(url='films/')

        res = sorted([Film(**i) for i in response.body], key=lambda x: x.id)
        expected = sorted(films, key=lambda x: x.id)

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == quantity
        assert res == expected

    async def test_pagination(
            self,
            storages_clean,
            upload_data_to_es_index,
            make_get_request,
            films_factory,
    ):
        """Test pagination at /api/v1/films/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_movies)

        quantity = 50
        _ = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=films_factory,
            index_name=test_settings.es_index_movies,
            es_id_field=test_settings.es_id_field
        ).__anext__()

        # Run #
        response = await make_get_request(
            url='films/',
            query_data={'page[size]': 20,
                        'page[number]': 3}
        )

        # Assertions #
        assert len(response.body) == 10

    async def test_get_by_id(
            self,
            storages_clean,
            upload_data_to_es_index,
            make_get_request,
            films_factory,
    ):
        """ Test GET film by id at /api/v1/films/{film_id}."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_movies)

        quantity = 5
        films = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=films_factory,
            index_name=test_settings.es_index_movies,
            es_id_field=test_settings.es_id_field
        ).__anext__()
        film = films[0]

        # Run #
        response = await make_get_request(url=f'films/{film.id}')

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert Film(**response.body) == film.dict()

    async def test_get_by_id_cached(
            self,
            storages_clean,
            upload_data_to_es_index,
            make_get_request,
            films_factory,
            redis_client,
    ):
        """Test caching for GET films at /api/v1/films/{film_id}."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_movies)

        quantity = 2
        films = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=films_factory,
            index_name=test_settings.es_index_movies,
            es_id_field=test_settings.es_id_field
        ).__anext__()
        target_film = films[0]

        await make_get_request(url=f'films/{target_film.id}')

        # Run #
        cached = await redis_client.get(target_film.id)

        # Assertions #
        assert Film(**json.loads(cached.decode('utf-8'))) == target_film

    async def test_not_found(
            self,
            make_get_request,
    ):
        """
        Test the response status when film is not found by id at
        /api/v1/films/{film_id}.
        """
        # Run #
        response = await make_get_request(url='films/test-uid')

        # Assertions #
        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Film with id test-uid not found'}
