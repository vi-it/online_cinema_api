"""
This module tests API that handles parametrized requests.
"""

import http
import random
import uuid

import faker
import pytest

from tests.functional.settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(
        es_write_data,
        make_get_request,
        query_data,
        expected_answer):
    """

    """
    # Setup #
    f = faker.Faker()
    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': f.pyfloat(right_digits=1, positive=True,
                                 min_value=1, max_value=10),
        'genre': [{'id': str(uuid.uuid4()), 'name': 'Action'},
                  {'id': str(uuid.uuid4()), 'name': 'Sci-Fi'}],
        'title': 'The Star',
        'description': 'New World',
        'actors_names': [f.name() for _ in range(random.randint(0, 4))],
        'writers_names': [f.name() for _ in range(random.randint(0, 3))],
        'directors': [{'id': str(uuid.uuid4()), 'name': f.name()}],
        'actors': [
            {'id': str(uuid.uuid4()), 'name': 'Ann'},
            {'id': str(uuid.uuid4()), 'name': 'Bob'}
        ],
        'writers': [
            {'id': str(uuid.uuid4()), 'name': 'Ben'},
            {'id': str(uuid.uuid4()), 'name': 'Howard'}
        ],
    } for _ in range(60)]
    await es_write_data(es_data, test_settings.es_index_movies, test_settings.es_id_field)

    response = await make_get_request('films/search/', query_data)

    assert response.status == expected_answer.get('status')
    assert len(response.body) == expected_answer.get('length')
