DC = docker compose
ENV = --env-file .env
APP_FILE = docker-compose/app.yaml
STORAGES_FILE = docker-compose/storages.yaml
NGINX_FILE = docker-compose/nginx.yaml

.PHONY: all
all:

	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${NGINX_FILE} ${ENV} up --build

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build