#!/bin/bash
set -e

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py init_site

exec gunicorn retro_cameras.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --timeout 120
