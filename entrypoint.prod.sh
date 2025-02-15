#!/usr/bin/env bash

echo "Running entrypoint.prod.sh"
cd backend
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 app.wsgi:application