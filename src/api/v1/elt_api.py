"""
The module is responsible for requesting data from Elasticsearch.
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src import models
from src.services import ELTService
from src.services.service_elt import get_elt_service


router = APIRouter()


@router.get('/film/', response_model=list[models.Film])
@router.get('/genre/', response_model=list[models.Genre])
@router.get('/person/', response_model=list[models.Person])
async def get_many_objects(
        request: Request,
        service: ELTService = Depends(get_elt_service)
):
    res = await service.get_many(str(request.url))
    return res


@router.get('/film/{film_id}', response_model=models.Film)
@router.get('/genre/{genre_id}', response_model=models.Genre)
@router.get('/person/{person_id}', response_model=models.Person)
async def get_object_by_id(
        obj_id: str,
        request: Request,
        service: ELTService = Depends(get_elt_service)
):
    res = await service.get_by_id(obj_id, str(request.url))
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Object not found')
    return res


# TODO: test the function and add examples of queries to README.md
@router.get('/film/search', response_model=models.Film)
@router.get('/genre/search', response_model=models.Genre)
@router.get('/person/search', response_model=models.Person)
async def get_query(
        query: str,
        page_size: int = Query(20, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        service: ELTService = Depends(get_elt_service)
):
    res = await service.search(query, page_size, page_number)
    return res

