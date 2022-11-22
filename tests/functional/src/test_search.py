import uuid

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
    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [{'id': str(uuid.uuid4()), 'name': 'Action'},
                  {'id': str(uuid.uuid4()), 'name': 'Sci-Fi'}],
        'title': 'The Star',
        'description': 'New World',
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'directors': [{'id': '101', 'name': 'Stan'}],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
    } for _ in range(60)]
    await es_write_data(es_data, test_settings.es_index_movies, test_settings.es_id_field)

    response = await make_get_request('films/search/', query_data)

    assert response.status == expected_answer.get('status')
    assert len(response.body) == expected_answer.get('length')
