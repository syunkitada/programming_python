#!/bin/bash -xe

sudo docker compose up db -d

cd backend

uv sync

source .venv/bin/activate

export FIRST_SUPERUSER=admin@example.com
export FIRST_SUPERUSER_PASSWORD=adminpass

python app/backend_pre_start.py
alembic upgrade head
python app/initial_data.py

export SECRET_KEY=secretkey
export FRONTEND_HOST=http://192.168.10.121:5173

fastapi dev --host 0.0.0.0 app/main.py
