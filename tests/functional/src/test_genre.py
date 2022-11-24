import pytest

from tests.functional.settings import test_settings
from tests.functional.models import Genre


@pytest.mark.asyncio
class TestGenreApi:

    async def test_get_list(
            self,
            storages_clean,
            create_es_index,
            es_write_data,
            make_get_request,
            genres_factory
    ):
        """
        Test get genres list /api/v1/genres/.
        """
        await storages_clean(index_name=test_settings.es_index_genres)

        es_data = [genres_factory().dict() for _ in range(10)]
        create_es_index(index_name=test_settings.es_index_genres)
        await es_write_data(es_data, test_settings.es_index_genres, test_settings.es_id_field)
        response = await make_get_request(url='genres/')

        assert response.status == 200
        assert len(response.body) == len(es_data)

    @pytest.mark.parametrize('expected_answer', [{'status': 200, 'length': 10}])
    async def test_cache_get_list(
            self,
            make_get_request,
            expected_answer
    ):
        """
        Test cache get genres /api/v1/genres/.
        """
        response = await make_get_request(url='genres/')

        assert response.status == expected_answer.get('status')
        assert len(response.body) == expected_answer.get('length')

    async def test_get_by_id(
            self,
            create_es_index,
            es_write_data,
            make_get_request,
            genres_factory
    ):
        """
        Test get genre by id /api/v1/genres/{genre_id}.
        """
        es_data = [genres_factory().dict() for _ in range(10)]
        create_es_index(index_name=test_settings.es_index_genres)
        await es_write_data(es_data, test_settings.es_index_genres, test_settings.es_id_field)
        genre = Genre(**es_data[0])
        response = await make_get_request(url=f'genres/{genre.id}')

        assert response.status == 200
        assert response.body == genre.dict(), "Get incorrect data"

    async def test_not_found(
            self,
            make_get_request,
    ):
        """
        Test status response when genre not found by id /api/v1/genres/{genre_id}.
        """
        response = await make_get_request(url=f'genres/test-uid')

        assert response.status == 404
