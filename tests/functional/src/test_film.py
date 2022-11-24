# import http
#
# import pytest
#
# from ..factories.film_factory import FilmFactory
# from pytest_factoryboy import register
# from tests.functional.settings import test_settings
#
# register(FilmFactory)
#
# @pytest.mark.asyncio
# # @pytest.mark.usefixtures('init_es_film_index')
# class TestFilmApi:
#     """"""
#
#     async def test_all_films(self, es_write_data, make_get_request, film_factory):
#
#         films = film_factory.create_batch(2)
#         await es_write_data([film.dict() for film in films], 'films',
#                             test_settings.es_id_field)
#
#         response = await make_get_request('films', None)
#         body = await response.json()
#
#         assert response.status == http.HTTPStatus.OK
#         assert len(body) > 1
#
#
