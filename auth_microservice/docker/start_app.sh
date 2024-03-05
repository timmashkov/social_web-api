#!/usr/bin/bash

alembic upgrade head

uvicorn runner:app --host 0.0.0.0 --port 8000 --reload
