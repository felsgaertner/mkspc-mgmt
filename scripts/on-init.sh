#!/bin/sh

python manage.py migrate
python manage.py loaddata traits.json booking_types.json
python manage.py createsuperuser
