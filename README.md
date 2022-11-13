## Ссылка на репозиторий
https://github.com/erlido/Async_API_sprint_2

## Технологии:
* Nginx;
* Fastapi;
* Postgresql;
* Elasticsearch;
* Redis.

## Установка и запуск проекта:

1. Клонировать репозиторий на локальную машину.
```https://github.com/erlido/Async_API_sprint_1.git```
   
2. Для удобства добавили `.env` в проект. При необходимости, заменить
   переменные окружения. Предполагается, что данные базы данных имеются
   на машине ревьюера.
   
3. Выполнить в корневой директории команду (после запуска приложение 
   автоматически начнет перенос данных из Postgres на сервер Elasticsearch.
   Процесс может занять несколько минут, информация будет выводиться в stdout):
```
docker-compose -f docker-compose.yml up --build
```
Возможен также запуск без приложения app
```
docker-compose -f docker-compose.dev.yml up --build
```
4. Документации API приведена на `http://127.0.0.1/api/openapi#/`.

## Авторы проекта
* [Ооржак Александр](https://github.com/Oorzhakau)
* [Щуров Виталий](https://github.com/erlido)
