"""
The module is responsible for requesting data about Actors,
Writers and Directors from Elasticsearch.
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src.core.config import settings
from src.db.redis import redis_cache
from src.models import Film, Person
from src.services import PersonService, get_person_service

router = APIRouter()


@router.get('/',
            response_model=list[Person],
            summary="Get person list",
            response_description="Return person list",
            )
@redis_cache(
    model=Person,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def get_persons_list(
        request: Request,
        page_size: int = Query(50, alias="page[size]", ge=1),
        page_number: int = Query(1, alias="page[number]", ge=1),
        service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """
    GET a list of persons according to the specified page size and number
    of items in a list.
    """
    res = await service.get_many(str(request.url),
                                 page_size,
                                 page_number)
    return res


@router.get('/{person_id}',
            response_model=Person,
            summary="Get person by id",
            response_description="Return person",
            )
@redis_cache(
    model=Person,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def get_object_by_id(
        request: Request,
        person_id: str,
        service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """
    Get person by id

    Examples:
    >>> http://127.0.0.1:8000/api/v1/persons/5bb0dd2c-3aff-4a2f-92f7-8cda3eb01ab0
    """
    res = await service.get_by_id(person_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Person with id {person_id} not found')
    return res


@router.get('/{person_id}/film/',
            response_model=list[Film],
            summary="Get person films",
            response_description="Return films",
            )
@redis_cache(
    model=Film,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def person_films(
        request: Request,
        person_id: str,
        page_size: int = Query(50, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        person_service: PersonService = Depends(get_person_service)
) -> list[Film]:
    """
    Get person films

    Examples:
    >>> http://127.0.0.1:8000/api/v1/persons/5bb0dd2c-3aff-4a2f-92f7-8cda3eb01ab0/film/
    """
    films = await person_service.get_films_by_person(
        person_id, page_size, page_number
    )
    return films


@router.get('/search/',
            response_model=list[Person],
            summary="Search person",
            response_description="Return persons",
            )
async def get_query(
        query: str | None,
        page_size: int = Query(default=50, alias="page[size]"),
        page_number: int = Query(default=1, alias="page[number]"),
        service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """
    Search persons by search query.

    Examples:
    >>> http://127.0.0.1:8000/api/v1/persons/search/?query=marina
    """
    res = await service.search(query=query, page_size=page_size, page_number=page_number)
    return res
