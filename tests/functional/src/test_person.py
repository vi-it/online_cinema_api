"""
This module tests API that handles person data.
"""
import http
import json
import random

import faker
import pytest
from tests.functional.models import Person
from tests.functional.settings import test_settings

g = faker.Faker()
SAMPLE_GENRES = [
    {'id': g.uuid4(), 'name': 'Action'},
    {'id': g.uuid4(), 'name': 'Sci-fi'},
    {'id': g.uuid4(), 'name': 'Drama'},
    {'id': g.uuid4(), 'name': 'Comedy'},
    {'id': g.uuid4(), 'name': 'Tragedy'},
    {'id': g.uuid4(), 'name': 'Horror'},
    {'id': g.uuid4(), 'name': 'Thriller'},
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
            upload_data_to_es_index,
            make_get_request,
            persons_factory,
            expected_answer
    ):
        """ Test GET person list at /api/v1/persons/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)

        quantity = 3
        persons = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=persons_factory,
            index_name=test_settings.es_index_persons,
            es_id_field=test_settings.es_id_field
        ).__anext__()

        # Run #
        response = await make_get_request(url='persons/')

        res = sorted([Person(**i) for i in response.body], key=lambda x: x.id)
        expected = sorted(persons, key=lambda x: x.id)

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == quantity
        assert res == expected

    async def test_pagination(
            self,
            storages_clean,
            upload_data_to_es_index,
            make_get_request,
            persons_factory,
    ):
        """Test pagination at /api/v1/persons/."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)

        quantity = 50
        _ = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=persons_factory,
            index_name=test_settings.es_index_persons,
            es_id_field=test_settings.es_id_field
        ).__anext__()

        # Run #
        response = await make_get_request(
            url='persons/',
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
            persons_factory,
    ):
        """Test GET person by id at /api/v1/persons/{person_id}."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)

        quantity = 5
        persons = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=persons_factory,
            index_name=test_settings.es_index_persons,
            es_id_field=test_settings.es_id_field
        ).__anext__()
        person = persons[0]

        # Run #
        response = await make_get_request(url=f'persons/{person.id}')

        # Assertions #
        assert response.status == 200
        assert Person(**response.body) == person.dict()

    async def test_get_by_id_cached(
            self,
            storages_clean,
            upload_data_to_es_index,
            make_get_request,
            persons_factory,
            redis_client,
    ):
        """Test caching for GET person at /api/v1/persons/{person_id}."""
        # Setup #
        await storages_clean(index_name=test_settings.es_index_persons)

        quantity = 2
        persons = await upload_data_to_es_index(
            quantity=quantity,
            obj_factory=persons_factory,
            index_name=test_settings.es_index_persons,
            es_id_field=test_settings.es_id_field
        ).__anext__()
        target_person = persons[0]

        await make_get_request(url=f'persons/{target_person.id}')

        # Run #
        cached = await redis_client.get(target_person.id)

        # Assertions #
        assert Person(**json.loads(cached.decode('utf-8'))) == target_person

    async def test_not_found(
            self,
            make_get_request,
    ):
        """
        Test the response status when person is not found by id at
        /api/v1/persons/{person_id}.
        """
        # Run #
        response = await make_get_request(url='persons/test-uid')

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

        await create_es_index(index_name=test_settings.es_index_persons)
        await es_write_data(es_data, test_settings.es_index_persons,
                            test_settings.es_id_field)
        person = Person(**es_data[0])

        # Run #
        response = await make_get_request(url='persons/search/?query=marina')

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
        await storages_clean(index_name=test_settings.es_index_movies)

        await create_es_index(index_name=test_settings.es_index_movies)

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

            data = {
                'id': f.uuid4(),
                'title': f.catch_phrase().title(),
                'description': f.text(max_nb_chars=100),
                'imdb_rating': imdb_rating,
                'genre': genres,
                'actors': actors,
                'directors': directors,
                'writers': writers,
                'actors_names': actors_names,
                'director': [director['name'] for director in directors],
                'writers_names': writers_names,
            }
            # Now, using the above data, generate a fake Elastic document:
            es_data.append(data)

        # 'Inject' the target actor into some random films:
        num_of_films = random.randint(1, len(es_data) // 2)
        starred = random.sample(es_data, k=num_of_films)
        for item in starred:
            item['actors'].append({'id': target_id, 'name': target_name})
            item['actors_names'].append(target_name)

        await es_write_data(es_data, test_settings.es_index_movies,
                            test_settings.es_id_field)

        # Run #
        response = await make_get_request(url=f'persons/{target_id}/film/')

        # Assertions #
        assert response.status == http.HTTPStatus.OK
        assert len(response.body) == num_of_films
