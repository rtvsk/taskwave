FROM python:3.11-slim

ENV POETRY_VERSION=1.8.3

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY ./ /app

RUN poetry config virtualenvs.in-project true

RUN poetry install

EXPOSE 8000
