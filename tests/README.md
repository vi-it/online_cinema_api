## Ссылка на репозиторий
https://github.com/erlido/Async_API_sprint_2

## Технологии:
* Docker;
* Pytest.

## Запуск тестов:
   
1. Для удобства добавили `.env` в проект. При необходимости, заменить
   переменные окружения. Предполагается, что данные базы данных имеются
   на машине ревьюера.
   
3. Выполнить в корневой директории команду `./tests/functional/` для запуска
функциональных тестов:

```
docker-compose -f docker-compose.yml up --build
```

Результаты тестирования должны быть аналогичны, указанным ниже:
```
============================= test session starts ==============================
platform linux -- Python 3.10.8, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /home/oorzhakau/proj/yandex/001_lessons/Async_API_sprint_2/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/oorzhakau/proj/yandex/001_lessons/Async_API_sprint_2/tests/functional, configfile: pytest.ini
plugins: factoryboy-2.5.0, Faker-15.3.2, asyncio-0.20.2
asyncio: mode=strict
collecting ... collected 19 items

src/test_film.py::TestFilmApi::test_get_list PASSED                      [  5%]
src/test_film.py::TestFilmApi::test_pagination PASSED                    [ 10%]
src/test_film.py::TestFilmApi::test_get_by_id PASSED                     [ 15%]
src/test_film.py::TestFilmApi::test_get_by_id_cached PASSED              [ 21%]
src/test_film.py::TestFilmApi::test_not_found PASSED                     [ 26%]
src/test_genre.py::TestGenreApi::test_get_list PASSED                    [ 31%]
src/test_genre.py::TestGenreApi::test_pagination PASSED                  [ 36%]
src/test_genre.py::TestGenreApi::test_get_by_id PASSED                   [ 42%]
src/test_genre.py::TestGenreApi::test_get_by_id_cached PASSED            [ 47%]
src/test_genre.py::TestGenreApi::test_not_found PASSED                   [ 52%]
src/test_person.py::TestPersonApi::test_get_list[expected_answer0] PASSED [ 57%]
src/test_person.py::TestPersonApi::test_pagination PASSED                [ 63%]
src/test_person.py::TestPersonApi::test_get_by_id PASSED                 [ 68%]
src/test_person.py::TestPersonApi::test_get_by_id_cached PASSED          [ 73%]
src/test_person.py::TestPersonApi::test_not_found PASSED                 [ 78%]
src/test_person.py::TestPersonApi::test_search PASSED                    [ 84%]
src/test_person.py::TestPersonApi::test_person_films PASSED              [ 89%]
src/test_search.py::test_search[query_data0-expected_answer0] PASSED     [ 94%]
src/test_search.py::test_search[query_data1-expected_answer1] PASSED     [100%]

============================= 19 passed in 17.66s ==============================
```