"""
The module is responsible for requesting data
about Films from Elasticsearch.
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src.core.config import settings
from src.db.redis import redis_cache
from src.models import Film
from src.services import FilmService, get_film_service

router = APIRouter()


@router.get('/',
            response_model=list[Film],
            summary="Get film list",
            response_description="Return films",
            )
@redis_cache(
    model=Film,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def get_films_list(
        request: Request,
        page_size: int = Query(20, alias="page[size]", ge=1),
        page_number: int = Query(1, alias="page[number]", ge=1),
        service: FilmService = Depends(get_film_service)
) -> list[Film]:
    """
    GET a list of films according to the specified page size and number
    of items in a list.
    """
    res = await service.get_many(str(request.url),
                                 page_size,
                                 page_number)
    return res


@router.get('/{film_id}',
            response_model=Film,
            summary="Get film by id",
            response_description="Return film",
            )
@redis_cache(
    model=Film,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def get_object_by_id(
        request: Request,
        film_id: str,
        service: FilmService = Depends(get_film_service)
) -> list[Film]:
    """
    Get film by id

    Examples:
    >>> http://127.0.0.1:8000/api/v1/films/3d825f60-9fff-4dfe-b294-1a45fa1e115d
    """
    res = await service.get_by_id(film_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Film with {film_id} not found')
    return res


@router.get('/search/',
            response_model=list[Film],
            summary="Search film",
            response_description="Return films",
            )
async def get_query(
        request: Request,
        query: str | None,
        page_size: int = Query(default=20, alias="page[size]"),
        page_number: int = Query(default=1, alias="page[number]"),
        service: FilmService = Depends(get_film_service)
) -> list[Film]:
    """
    Search films by search query.

    Examples:
    >>> http://127.0.0.1:8000/api/v1/films/search/?query=star
    """
    service.get_index(str(request.url))
    res = await service.search(query=query, page_size=page_size, page_number=page_number)
    return res
