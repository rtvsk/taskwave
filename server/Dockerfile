FROM python:3.11.1

ENV POETRY_VERSION=1.8.3

ENV ENV_FILE=".env"

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY ./ /app

RUN poetry config virtualenvs.in-project true

RUN poetry install

# RUN poetry run alembic upgrade head

EXPOSE 8000

