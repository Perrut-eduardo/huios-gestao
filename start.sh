#!/usr/bin/env bash
set -euo pipefail
python manage.py migrate --noinput
python manage.py criar_perfis
python manage.py criar_usuario_demo
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-10000}" --workers 1 --timeout 120 --access-logfile -
