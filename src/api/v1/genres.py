"""
The module is responsible for requesting data about
Genres Film from Elasticsearch.
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src.core.config import settings
from src.db.redis import redis_cache
from src.models import Genre
from src.services import GenreService, get_genre_service

router = APIRouter()


@router.get('/',
            response_model=list[Genre],
            summary="Get genres",
            response_description="Return genres",
            )
@redis_cache(
    model=Genre,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def get_genres_list(
        request: Request,
        page_size: int = Query(50, alias="page[size]", ge=1),
        page_number: int = Query(1, alias="page[number]", ge=1),
        service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """
    GET a list of genres according to the specified page size and number
    of items in a list.
    """
    res = await service.get_many(str(request.url),
                                 page_size,
                                 page_number)
    return res


@router.get('/{genre_id}',
            response_model=Genre,
            summary="Get genre by id",
            response_description="Return genre",
            )
@redis_cache(
    model=Genre,
    expired=settings.CACHE_EXPIRE_IN_SECONDS
)
async def get_object_by_id(
        request: Request,
        genre_id: str,
        service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """
    Get genre by id

    Examples:
    >>> http://127.0.0.1:8000/api/v1/genres/120a21cf-9097-479e-904a-13dd7198c1dd
    """
    res = await service.get_by_id(genre_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Genre with id {genre_id} not found')
    return res
