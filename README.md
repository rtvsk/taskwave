cd server

make venv
py -m venv venv

activate venv
source ./venv/bin/activate


install dependencies
pip install -r requirements_my.txt

run migrations
alembic upgrade head

run server
uvicorn src.main:app --reload