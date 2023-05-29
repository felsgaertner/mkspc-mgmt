#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --ini /uwsgi.ini
