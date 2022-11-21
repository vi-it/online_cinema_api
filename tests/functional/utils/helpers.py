import json


def get_es_bulk_query(es_data: list, index_name: str, es_id_field: str) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index_name,
                                  '_id': row[es_id_field]}}),
            json.dumps(row)
        ])
    return bulk_query
