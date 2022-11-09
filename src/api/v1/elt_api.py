"""
The module is responsible for requesting data from Elasticsearch.
"""
import typing
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src import models
from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.db.redis import redis_cache
from src.services import ELTService
from src.services.person import PersonService, get_person_service
from src.services.service_elt import get_elt_service

CINEMA_MODEL = typing.TypeVar('CINEMA_MODEL',
                              models.Film,
                              models.Person,
                              models.Genre)

router = APIRouter()


@router.get('/film/', response_model=list[models.Film])
@router.get('/genre/', response_model=list[models.Genre])
@router.get('/person/', response_model=list[models.Person])
@redis_cache(expired=CACHE_EXPIRE_IN_SECONDS)
async def get_many_objects(
        request: Request,
        page_size: int = Query(20, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        service: ELTService = Depends(get_elt_service)
) -> list[CINEMA_MODEL]:
    res = await service.get_many(str(request.url),
                                 page_size,
                                 page_number)
    return res


@router.get('/person/{person_id}/film/')
@redis_cache(expired=CACHE_EXPIRE_IN_SECONDS)
async def person_films(
        request: Request,
        person_id: str,
        page_size: int = Query(20, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        person_service: PersonService = Depends(get_person_service)
) -> list[models.Film]:
    """
    Get person films

    Examples:
    >>> http://127.0.0.1:8000/api/v1/person/5bb0dd2c-3aff-4a2f-92f7-8cda3eb01ab0/film/
    """
    films = await person_service.get_films_by_person(
        person_id, page_size, page_number
    )
    return films


@router.get('/film/{film_id}', response_model=models.Film)
@redis_cache(expired=CACHE_EXPIRE_IN_SECONDS)
async def get_object_by_id(
        request: Request,
        film_id: str,
        service: ELTService = Depends(get_elt_service)
) -> list[CINEMA_MODEL]:
    """
    Get item by id

    Examples:
    >>> http://127.0.0.1:8000/api/v1/film/3d825f60-9fff-4dfe-b294-1a45fa1e115d
    """
    res = await service.get_by_id(film_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Object not found')
    return res

@router.get('/genre/{genre_id}', response_model=models.Genre)
@redis_cache(expired=CACHE_EXPIRE_IN_SECONDS)
async def get_object_by_id(
        request: Request,
        genre_id: str,
        service: ELTService = Depends(get_elt_service)
) -> list[CINEMA_MODEL]:
    """
    Get item by id

    Examples:
    >>> http://127.0.0.1:8000/api/v1/genre/120a21cf-9097-479e-904a-13dd7198c1dd
    """
    res = await service.get_by_id(genre_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Object not found')
    return res\

@router.get('/person/{person_id}', response_model=models.Person)
@redis_cache(expired=CACHE_EXPIRE_IN_SECONDS)
async def get_object_by_id(
        request: Request,
        person_id: str,
        service: ELTService = Depends(get_elt_service)
) -> list[CINEMA_MODEL]:
    """
    Get item by id

    Examples:
    >>> http://127.0.0.1:8000/api/v1/person/5bb0dd2c-3aff-4a2f-92f7-8cda3eb01ab0
    """
    res = await service.get_by_id(person_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Object not found')
    return res


@router.get('/film/search/', response_model=list[models.Film])
@router.get('/person/search/', response_model=list[models.Person])
async def get_query(
        request: Request,
        query: str | None,
        page_size: int = Query(default=20, alias="page[size]"),
        page_number: int = Query(default=1, alias="page[number]"),
        service: ELTService = Depends(get_elt_service)
) -> list[CINEMA_MODEL]:
    """
    Search films or persons by search query.

    Examples:
    >>> http://127.0.0.1:8000/api/v1/person/search/?query=marina
    >>> http://127.0.0.1:8000/api/v1/film/search/?query=star
    """
    service.get_index(str(request.url))
    res = await service.search(query=query, page_size=page_size, page_number=page_number)
    return res
