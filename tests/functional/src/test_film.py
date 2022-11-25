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

    @pytest.mark.parametrize('expected_answer',
                             [{'status': http.HTTPStatus.OK, 'length': 3}])
    async def test_cache_get_list(
        self,
        make_get_request,
        expected_answer,
    ):
        """Test caching for GET films at /api/v1/films/."""
        # Run #
        response = await make_get_request(url='films/')

        # Assertions #
        assert response.status == expected_answer.get('status')
        assert len(response.body) == expected_answer.get('length')

    async def test_get_by_id(
            self,
            create_es_index,
            es_write_data,
            make_get_request,
            films_factory,
    ):
        """ Test GET film by id at /api/v1/films/{film_id}."""
        # Setup #
        es_data = [films_factory().dict() for _ in range(5)]
        create_es_index(index_name=test_settings.es_index_movies)
        await es_write_data(es_data, test_settings.es_index_movies,
                            test_settings.es_id_field)
        film = Film(**es_data[0])

        # Run #
        response = await make_get_request(url=f'films/{film.id}')

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert Film(**response.body) == film.dict()

    async def test_not_found(
            self,
            make_get_request,
    ):
        """
        Test the response status when film is not found by id at
        /api/v1/films/{film_id}.
        """
        # Run #
        response = await make_get_request(url=f'films/test-uid')

        # Assertions #
        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Film with id test-uid not found'}
