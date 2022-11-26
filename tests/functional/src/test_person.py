"""
This module tests API that handles person data.
"""

import http
import random

import faker
import pytest

from tests.functional.models import Person
from tests.functional.settings import test_settings

g = faker.Faker()
SAMPLE_GENRES = [
    {g.uuid4(): 'Action'},
    {g.uuid4(): 'Sci-fi'},
    {g.uuid4(): 'Drama'},
    {g.uuid4(): 'Comedy'},
    {g.uuid4(): 'Tragedy'},
    {g.uuid4(): 'Horror'},
    {g.uuid4(): 'Thriller'},
]
# Elastic fake documents won't have more genres than this number:
MAX_GENRES = len(SAMPLE_GENRES) // 2

@pytest.mark.asyncio
class TestPersonApi:

    @pytest.mark.parametrize('expected_answer',
                             [{'status': 200, 'length': 50}])
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

    @pytest.mark.parametrize('expected_answer',
                             [{'status': http.HTTPStatus.OK, 'length': 3}])
    async def test_cache_get_list(
            self,
            make_get_request,
            expected_answer
    ):
        """Test caching for GET person at /api/v1/persons/."""
        # Run #
        response = await make_get_request(url='persons/')

        # Assertions #
        assert response.status == expected_answer.get('status')
        assert len(response.body) == expected_answer.get('length')

    async def test_get_by_id(
            self,
            create_es_index,
            es_write_data,
            make_get_request,
            persons_factory,
    ):
        """Test GET person by id at /api/v1/persons/{person_id}."""
        # Setup #
        es_data = [persons_factory().dict() for _ in range(5)]
        create_es_index(index_name=test_settings.es_index_persons)
        await es_write_data(es_data, test_settings.es_index_persons,
                            test_settings.es_id_field)
        person = Person(**es_data[0])

        # Run #
        response = await make_get_request(url=f'persons/{person.id}')

        # Assertions #
        assert response.status == 200
        assert Person(**response.body) == person.dict()

    async def test_not_found(
            self,
            make_get_request,
    ):
        """
        Test the response status when when person is not found by id at
        /api/v1/persons/{person_id}.
        """
        # Run #
        response = await make_get_request(url=f'persons/test-uid')

        # Assertions #
        assert response.status == http.HTTPStatus.NOT_FOUND
        assert response.body == {'detail': 'Person with id test-uid not found'}

    async def test_search(
            self,
            storages_clean,
            create_es_index,
            es_write_data,
            make_get_request,
            persons_factory,
    ):
        """
        Test search with a parametrized request at
        /api/v1/persons/search/?query=marina.
        """
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)

        test_name = ['Marina', 'Ivan', 'Alexander', 'Ksysha', 'Vladimir']
        es_data = [persons_factory(name=n).dict() for n in test_name]

        create_es_index(index_name=test_settings.es_index_persons)
        await es_write_data(es_data, test_settings.es_index_persons,
                            test_settings.es_id_field)
        person = Person(**es_data[0])

        # Run #
        response = await make_get_request(url=f'persons/search/?query=marina')

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == 1
        assert response.body[0] == person.dict()

    async def test_person_films(
            self,
            storages_clean,
            create_es_index,
            es_write_data,
            make_get_request,
    ):
        """Test GET person's films at /api/v1/persons/{person_id}/film/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)
        await storages_clean(index_name=test_settings.es_index_movies)

        create_es_index(index_name=test_settings.es_index_movies)

        f = faker.Faker()
        # Create an actor whose films will be requested:
        target_name, target_id = f.name(), f.uuid4()

        es_data = []
        for _ in range(10):
            # Generate random data about actors:
            actors = [{'id': f.uuid4(), 'name': f.name()}
                      for _ in range(random.randint(1, 4))]
            actors_names = [act['name'] for act in actors]

            # Generate random data about writers:
            writers = [{'id': f.uuid4(), 'name': f.name()}
                       for _ in range(random.randint(1, 4))]
            writers_names = [wri['name'] for wri in writers]

            imdb_rating = f.pyfloat(right_digits=1, positive=True,
                                    min_value=1, max_value=10)

            # Generate random data about directors:
            directors = [
                {'id': f.uuid4(), 'name': f.name()} for _ in range(2)
            ]

            # Pick some random genres:
            genres = random.sample(
                SAMPLE_GENRES, k=random.randint(1, MAX_GENRES)
            )

            # Now, using the above data, generate a fake Elastic document:
            data = {
                'id': f.uuid4(),
                'imdb_rating': imdb_rating,
                'genre': genres,
                'title': f.catch_phrase().title(),
                'description': f.text(max_nb_chars=100),
                'actors_names': actors_names,
                'writers_names': writers_names,
                'directors': directors,
                'actors': actors,
                'writers': writers,
            }
            es_data.append(data)

        # 'Inject' the target actor into some random films:
        num_of_films = random.randint(1, len(es_data)//2)
        starred = random.sample(es_data, k=num_of_films)
        for item in starred:
            item['actors'].append({'id': target_id, 'name': target_name})
            item['actors_names'].append(target_name)

        await es_write_data(es_data, test_settings.es_index_movies,
                            test_settings.es_id_field)

        await es_write_data(es_data, test_settings.es_index_movies,
                            test_settings.es_id_field)

        # Run #
        response = await make_get_request(url=f'persons/{target_id}/film/')

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == num_of_films

