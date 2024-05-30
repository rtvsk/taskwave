FROM python:3.11.1

ENV POETRY_VERSION=1.8.3

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./.env ./alembic.ini ./pytest.ini ./

RUN poetry config virtualenvs.in-project true

RUN poetry install

# RUN poetry shell
# ENV PYTHONPATH=/app/src

WORKDIR /app/src

COPY ./src ./

WORKDIR /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
