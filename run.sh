#!/bin/bash

python manage.py collectstatic --no-input
PORT=8020
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --access-logfile - \
    --timeout 300 \
    gateway.wsgi:application -w 2
