## Authors
* [Alexander Oorzhak](https://github.com/Oorzhakau)
* [Vitaly Shchurov](https://github.com/erlido)

## Technologies:
* Elasticsearch;
* FastAPI;
* Nginx;
* Postgresql;
* Pytest;
* Redis.

## Setup (database data is not present in the repository):

1. Clone the repository:
```https://github.com/erlido/Async_API_sprint_1.git```
   
2. Create an '.env' file based on '.env.example'. Change <PWD> for the
database volume. Change other values, if needed.
   
3. Run the following command from the project directory (after starting,
   the app will automatically begin transferring data from PostgreSQL
   to Elasticsearch. This may take a little while, the logs will be
   printed to stdout):
```
docker-compose -f docker-compose.yml up --build
```
To run without the application, type:
```
docker-compose -f docker-compose.dev.yml up --build
```
4. OpenApi documentation is available at `http://127.0.0.1/api/openapi#/`.

