# Development Setup

To run all components (OQT/API, Database, Website) in Docker containers simply run:

```bash
docker-compose -f docker-compose.development.yml up -d
```

After all services are up they are available under:

- Website: [http://127.0.0.1:8081/](http://127.0.0.1:8081/)
- API: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
- Database: `host=localhost port=5445 dbname=oqt user=oqt password=oqt`


## Database

A database for development purposes is provided as Dockerfile. To build and run a already configured image run:

```bash
docker-compose -f docker-compose.development.yml up -d oqt-database
```

When the database container is running for the first time it takes a couple of minutes until the database is initialized and ready to accept connections.
Check the progress with `docker logs oqt-database`.

To reinitialize or update the database make sure to delete the volume and rebuild the image. This will delete all data in the database:

```bash
# Make sure that your git is up2date, e.g. git pull
docker stop oqt-database && docker rm oqt-database
docker volume rm ohsome-quality-analyst_oqt-dev-pg_data
docker-compose -f docker-compose.development.yml up -d --build oqt-database
```

> To get access to a running database on a remote server please reach out.


## OQT Python package

### Requirements

- Python 3.8+
- Poetry 1.1.0+

This project uses [Poetry](https://python-poetry.org/docs/) for packaging and dependencies management. Please make sure it is installed on your system.


### Installation

```bash
cd workers/
poetry install
poetry shell  # Spawns a shell within the virtual environment.
pre-commit install  # Install pre-commit hooks.
# Hack away
```

> Note: If during the installation of `matplotlib` an error occurs the solution could be to install `freetype`. See the install documentation of `matplotlib`: https://github.com/matplotlib/matplotlib/blob/master/INSTALL.rst#freetype-and-qhull


### Configuration

**Local database:**

For local development no additional configuration is required. Per default OQT will connect to the database definied in `docker-compose.development.yml`.

**Remote database:**

If access to a remote database is required following environment variables need to be set:

```bash
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_SCHEMA
```

> Tip: Above lines can be written to a file (E.g. `.env`), prefixed with `export` and sourced (`source .env`) to make them available to current environment.

Windows user can set those environment variables with following command `setx POSTGRES_DB`


**ohsome API:**

The URL to a specific ohsome API can be set with the environment variable `OHSOME_API`. It defaults to [https://api.ohsome.org/v1/](https://api.ohsome.org/v1/)


### Usage

CLI:
```bash
oqt --help
```

API:
```bash
uvicorn ohsome_quality_analyst.api:app --reload
```

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and check out the endpoints.


### Tests

Tests are written using the [unittest library](https://docs.python.org/3/library/unittest.html).
The test runner is [pytest](https://docs.pytest.org/en/stable/).
Tests are seperated into integration tests and unit tests.
Unit tests should run without having access to the database or services the internet (e.g. ohsome API).

```bash
cd workers/
pytest tests
```