#!/bin/bash

python manage.py collectstatic --no-input
PORT=8021
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --access-logfile - \
    --timeout 3600 \
    --worker-class gevent \
    --workers 4\
    gateway.wsgi:application
