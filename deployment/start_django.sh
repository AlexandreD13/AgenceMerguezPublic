#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input --clear
gunicorn --config deployment/gunicorn.py agence.wsgi:application --bind 0.0.0.0:8000
