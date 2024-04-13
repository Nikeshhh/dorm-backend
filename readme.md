# Dorm backend

Бэкэнд приложения системы для общежития.

## Установка

Клонировать репозиторий
```
git clone ...
```

Установить прекоммиты
```
pre-commit install
```

Запустить базу данных в контейнере
```
docker compose -f .\docker-compose\storages.yaml --env-file .env  up --build -d
```

Запустить приложение внутри контейнера
```
docker compose -f .\docker-compose\app.yaml --env-file .env  up --build -d
```