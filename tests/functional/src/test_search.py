"""
This module tests API that handles parametrized requests.
"""

import http
import random

import faker
import pytest
from tests.functional.settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'Star'},
            {'status': http.HTTPStatus.OK, 'length': 20}
        ),
        (
            {'query': 'Mashed potato'},
            {'status': http.HTTPStatus.OK, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(
        storages_clean,
        es_write_data,
        make_get_request,
        query_data,
        expected_answer):
    """Test GET films with a parametrized query at films/search/."""
    # Setup #
    await storages_clean(index_name=test_settings.es_index_movies)

    f = faker.Faker()
    es_data = [{
        'id': f.uuid4(),
        'imdb_rating': f.pyfloat(right_digits=1, positive=True,
                                 min_value=1, max_value=10),
        'genre': [{'id': f.uuid4(), 'name': 'Action'},
                  {'id': f.uuid4(), 'name': 'Sci-Fi'}],
        'title': 'The Star',
        'description': f.text(max_nb_chars=100),
        'actors_names': [f.name() for _ in range(random.randint(0, 4))],
        'writers_names': [f.name() for _ in range(random.randint(0, 3))],
        'directors': [{'id': f.uuid4(), 'name': f.name()}],
        'actors': [
            {'id': f.uuid4(), 'name': f.name()},
            {'id': f.uuid4(), 'name': f.name()}
        ],
        'writers': [
            {'id': f.uuid4(), 'name': f.name()},
            {'id': f.uuid4(), 'name': f.name()}
        ],
    } for _ in range(20)]
    await es_write_data(es_data, test_settings.es_index_movies,
                        test_settings.es_id_field)

    # Run #
    response = await make_get_request('films/search/', query_data)

    # Assertions #
    assert response.status == expected_answer.get('status')
    assert len(response.body) == expected_answer.get('length')
