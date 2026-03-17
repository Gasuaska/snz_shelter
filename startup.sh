#!/bin/sh
. venv/bin/activate

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn shelter_project.wsgi:application --bind 0.0.0.0:8000
