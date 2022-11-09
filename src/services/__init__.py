__all__ = [
    'FilmService',
    'GenreService',
    'PersonService',
    'get_film_service',
    'get_genre_service',
    'get_person_service',
]

from src.services.film import get_film_service, FilmService
from src.services.genre import get_genre_service, GenreService
from src.services.person import get_person_service, PersonService
