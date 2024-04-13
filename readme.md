# Template for Django REST Framework application

Repository for DRF template.

Contains all basic requirements to start application development.

Contains ready-to-use docker infrastructure.

Allows to run application either locally or inside container.

## Installation

Clone repository
```
git clone ...
```

Install pre-commit hooks into git
```
pre-commit install
```

Run database inside container
```
docker compose -f .\docker-compose\storages.yaml --env-file .env  up --build -d
```

Run application inside container
```
docker compose -f .\docker-compose\app.yaml --env-file .env  up --build -d
```

## Pre-installed django apps

* corsheaders
* rest_framework
* django-environ
* psycopg2

## Pre-configured settings

To run application with your custom settings, you should:

* create `local.py` file, inside `settings` directory
* import all variables from `main.py` settings
* rewrite all necessary settings
* replace `__init__.py` import, inside settings directory

There are example `local_example.py` file, inside settings directory.