DC = docker compose
ENV = --env-file .env
APP_FILE = docker-compose/app.yaml
STORAGES_FILE = docker-compose/storages.yaml
NGINX_FILE = docker-compose/nginx.yaml
LOGS = docker logs
APP_CONTAINER = main-app
CELERY_BEAT_CONTAINER = celery-beat-app
CELERY_WORKER_CONTAINER = celery-worker-app
NGINX_CONTAINER = nginx-server
DB_CONTAINER = db
RABBIT_CONTAINER = rabbitmq

.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${NGINX_FILE} ${ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${NGINX_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: nginx-logs
nginx-logs:
	${LOGS} ${NGINX_CONTAINER} -f

.PHONY: db-logs
db-logs:
	${LOGS} ${DB_CONTAINERS} -f

.PHONY: cb-logs
cb-logs:
	${LOGS} ${CELERY_BEAT_CONTAINER} -f

.PHONY: cw-logs
cw-logs:
	${LOGS} ${CELERY_WORKER_CONTAINER} -f

.PHONY: rabbit-logs
rabbit-logs:
	${LOGS} ${RABBIT_CONTAINER} -f