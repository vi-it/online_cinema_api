from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.services.film import FilmService, ETLService, get_film_service, \
    get_elt_service

router = APIRouter()


class Film(BaseModel):
    """API Response model for movies."""
    id: str
    title: str


# @router.get('/{film_id}', response_model=Film)
# async def film_details(
#         film_id: str, film_service: FilmService = Depends(get_film_service)
# ) -> Film:
#     film = await film_service.get_by_id(film_id)
#     if not film:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
#                             detail='film not found')
#     return Film(id=film.id, title=film.title)


async def get_by_id(
        obj_id: str,
        service: ETLService = Depends(get_film_service)
):
    obj = await service.get_by_id(obj_id)
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')
    return obj

@router.get('/{film_id}', response_model=Film)
async def get_film_by_id(
    obj_id: str
):
    res = await get_by_id(obj_id)
    return res
