__all__ = [
    'FilmService',
    'GenreService',
    'PersonService',
    'get_film_service',
    'get_genre_service',
    'get_person_service',
]

from src.services.film import FilmService, get_film_service
from src.services.genre import GenreService, get_genre_service
from src.services.person import PersonService, get_person_service
