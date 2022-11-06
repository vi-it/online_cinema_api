from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src import models
from src.services.film import FilmService, get_film_service
from src.services import ELTService
from src.services.service_elt import get_elt_service


router = APIRouter()


@router.get('/{film_id}', response_model=models.Film)
async def get_obj_by_id(
        obj_id: str,
        service: ELTService = Depends(get_elt_service)
):
    obj = await service.get_by_id(obj_id)
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')
    return obj

# @router.get('/', response_model=Film)
# async def get_films(
#     obj_id: str
# ):
#     res = await get_by_id(obj_id)
#     return res
