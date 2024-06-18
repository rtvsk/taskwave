FROM python:3.11-slim

ENV POETRY_VERSION=1.8.3
ENV SMTP_HOST=$SMTP_HOST
ENV SMTP_PORT=$SMTP_PORT
ENV SMTP_EMAIL=$SMTP_EMAIL
ENV SMTP_PASSWORD=$SMTP_PASSWORD

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY ./ /app

RUN poetry config virtualenvs.in-project true

RUN poetry install

EXPOSE 8000

