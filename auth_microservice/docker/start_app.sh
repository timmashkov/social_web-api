#!/usr/bin/bash

alembic upgrade head

cd src/

uvicorn main:start_app --host 0.0.0.0 --port 3333 --reload
