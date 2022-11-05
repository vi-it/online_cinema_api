from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from src.services.person import PersonService, get_person_service

router = APIRouter()


class Person(BaseModel):
    """API Response model for person."""
    id: str
    full_name: str
    role: str | None
    film_ids: list[str | None]


class Film(BaseModel):
    """API Response model for movies."""
    id: str
    title: str
    imdb_rating: float


@router.get('/<person_id>/')
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> Optional[Person]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/search/')
async def person_details(
        query: str,
        page_size: int = Query(20, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    persons = await person_service.search(query, page_size, page_number)
    return persons


@router.get('/<person_id>/film/')
async def person_films(
        person_id: str,
        page_size: int = Query(20, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        person_service: PersonService = Depends(get_person_service)
) -> list[Film]:
    films = await person_service.get_films_by_person(
        person_id, page_size, page_number
    )
    return [Film(id=film.id,
                 title=film.title,
                 imdb_rating=film.imdb_rating)
            for film in films]
