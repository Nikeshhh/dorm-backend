FROM python:3.12.4-slim-bullseye as python-base

# create environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE= \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/var/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/var/pysetup" \
    VENV_PATH="/var/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# build dependencies
FROM python-base as builder
RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR $PYSETUP_PATH

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev


# build production image
FROM python-base as production


COPY --from=builder $VENV_PATH $VENV_PATH
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./core /app/core
COPY ./manage.py /app/
WORKDIR /app

CMD ["sh", "../entrypoint.sh"]

