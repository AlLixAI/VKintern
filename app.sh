#!/usr/bin/env bash

chmod +x app.sh

alembic upgrade head

gunicorn rest.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000