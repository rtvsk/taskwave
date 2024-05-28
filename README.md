cd server

poetry config virtualenvs.in-project true. (Для установки .env в проект)
poetry install 
poetry shell (для подключения) 
exit (для отключения)

run migrations
alembic upgrade head

run server
uvicorn src.main:app --reload