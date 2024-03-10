#!/usr/bin/bash

alembic upgrade head

cd app_src/

uvicorn main:server_api --host 0.0.0.0 --port 2222 --reload
