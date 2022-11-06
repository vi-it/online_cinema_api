from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from src import models
from src.services.film import FilmService, get_film_service
from src.services import ELTService
from src.services.service_elt import get_elt_service

router = APIRouter()


@router.get('/film/{film_id}', response_model=models.Film)
@router.get('/genre/{genre_id}', response_model=models.Genre)
@router.get('/person/{person_id}', response_model=models.Person)
async def get_obj_by_id(
        obj_id: str,
        request: Request,
        service: ELTService = Depends(get_elt_service)
):

    obj = await service.get_by_id(obj_id, str(request.url))
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')
    return obj

