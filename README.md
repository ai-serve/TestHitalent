# Q&A for HiTalent

*Read carefully to deploy and test*

## Deployment

## Docker compose project

### Known issues

1. If needed, change `platform: linux/amd64` in [docker compose](docker-compose.yaml) to a correct platform when
running the compose project on any other platform (e.g., Mac on Apple M* CPUs).
2. Change port forwarding rules in [docker compose](docker-compose.yaml) 
if you have port conflicts. Also, match with [Dockerfile](/Dockerfile) 
and [tests' configuration](/test/config.py) where needed.
3. Check that local [.env](core.env) 
and compose project's `postgres` service's environment match 
if you change either (and/or if you've changed `postgres` service's ports, as per issue 2).

### App start up

Bash run `docker compose up -d --build` from project directory to spin up new containers (core and postgres services)
as per the [YAML config](docker-compose.yaml).

Alternatively, bash run `uvicorn core.main.app:APP --host 0.0.0.0 --port 7070 --env-file core.env`.

## Testing

Tests are all preconfigured with pytest fixtures, a vital part of which is Alembic migrations setup
(both adding tables beforehand and deleting tables afterward).

You'll find tests in both [test_orm](./test/test_orm.py) and [test_api](./test/test_api.py).
You'll find Alembic migration settings in pytest fixture defined in [conftest](./test/conftest.py).

Install [test requirements](./test/test_requirements.txt) and bash run `pytest`.

## API endpoints

Check FastAPI generated docs at (currently) `0.0.0.0:7070/docs`.

## Notes

- Fields `created_at` are populated via sqlalchemy sessions, 
and are not forced (i.e., are optional) in Pydantic validation models.
To that: they are calculated with `datetime.datetime.now(datetime.UTC)` on object creation.
