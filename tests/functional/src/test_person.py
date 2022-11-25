"""
This module tests API that handles person data.
"""

import http

import pytest

from tests.functional.models import Person
from tests.functional.settings import test_settings


@pytest.mark.asyncio
class TestPersonApi:

    @pytest.mark.parametrize('expected_answer', [{'status': 200, 'length': 50}])
    async def test_get_list(
            self,
            storages_clean,
            create_es_index,
            es_write_data,
            make_get_request,
            persons_factory,
            expected_answer
    ):
        """ Test GET person list at /api/v1/persons/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)

        quantity = 3
        persons = persons_factory.create_batch(quantity)
        persons_num = len(persons)

        create_es_index(index_name=test_settings.es_index_persons)

        await es_write_data(
            [person.dict() for person in persons],
            test_settings.es_index_persons,
            test_settings.es_id_field
        )

        # Run #
        response = await make_get_request(url='persons/')

        res = sorted([Person(**i) for i in response.body], key=lambda x: x.id)
        expected = sorted(persons, key=lambda x: x.id)

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert persons_num == quantity
        assert len(response.body) == persons_num
        assert res == expected

#     @pytest.mark.parametrize('expected_answer', [{'status': 200, 'length': 50}])
#     async def test_cache_get_list(
#             self,
#             make_get_request,
#             expected_answer
#     ):
#         """
#         Test cache get person lest /api/v1/persons/.
#         """
#         response = await make_get_request(url='persons/', query_data="")
#
#         assert response.status == expected_answer.get('status')
#         assert len(response.body) == expected_answer.get('length')
#
#     async def test_get_by_id(
#             self,
#             create_es_index,
#             es_write_data,
#             make_get_request,
#             persons_factory,
#     ):
#         """
#         Test get person by id /api/v1/persons/{person_id}.
#         """
#         es_data = [persons_factory().dict() for _ in range(10)]
#         create_es_index(index_name="persons")
#         await es_write_data(es_data, test_settings.es_index_persons, test_settings.es_id_field)
#         person = Person(**es_data[0])
#         response = await make_get_request(url=f'persons/{person.id}')
#
#         assert response.status == 200
#         assert response.body == person.dict(), "Get incorrect data"
#
#     async def test_not_found(
#             self,
#             make_get_request,
#     ):
#         """
#         Test status response when person not found by id /api/v1/persons/{person_id}.
#         """
#         response = await make_get_request(url=f'persons/test-uid')
#
#         assert response.status == 404
#
#     async def test_search(
#             self,
#             storages_clean,
#             create_es_index,
#             es_write_data,
#             make_get_request,
#             persons_factory,
#     ):
#         """
#         Test search /api/v1/persons/search/?query=marina.
#         """
#         await storages_clean(index_name=test_settings.es_index_persons)
#
#         test_name = ["Marina", "Ivan", "Alexander", "Ksysha", "Vladimir"]
#         es_data = [persons_factory(name=test_name[i]).dict() for i in range(5)]
#         create_es_index(index_name=test_settings.es_index_persons)
#         await es_write_data(es_data, test_settings.es_index_persons, test_settings.es_id_field)
#         person = Person(**es_data[0])
#         response = await make_get_request(url=f'persons/search/?query=marina')
#
#         assert response.status == 200
#         assert response.body[0] == person.dict(), "Response involve incorrect data"
#
#     async def test_person_films(self):
#         """
#         Test get person films /api/v1/persons/{person_id}/film/
#         """
#         ... # todo: дописать тест
