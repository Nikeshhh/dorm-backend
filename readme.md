# Приложения для общежития - Моя ВКР

Бэкэнд приложения системы для общежития.

Система автоматизирует такие процессы как:

* Формирование графиков дежурств
* Корректировка графиков дежурств
* Регистрация результатов проведения санитарных проверок
* Обслуживание журнала регистрации работы прачечной
* Обслуживание журнала заявок на ремонт

## Установка

Клонировать репозиторий
```
git clone https://github.com/Nikeshhh/dorm-backend.git
```

Заполнить `.env` файл
```
POSTGRES_DB=defaultdb - название БД
POSTGRES_USER=postgresql - имя пользователя БД
POSTGRES_PASSWORD=qwerty - пароль пользователя БД
POSTGRES_HOST=db - хост БД
POSTGRES_PORT=5432 - порт БД (при запуске в локале изменить)
DJANGO_PORT=8000 - порт приложения
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

Запустутить production сервер
```
docker compose -f .\docker-compose\storages.yaml -f .\docker-compose\app.yaml -f .\docker-compose\nginx.yaml  --env-file .env  up --build
```