from fastapi import APIRouter
from pydantic import BaseModel

# Объект router, в котором регистрируем обработчики
router = APIRouter()

class Film(BaseModel):
    """API Response model for movies."""
    id: str
    title: str

@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str) -> Film:
    return Film(id='some_id', title='some_title')
