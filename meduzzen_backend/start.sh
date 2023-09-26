#!/bin/sh
# Creating migrations if they are
python manage.py makemigrations
# Apply migrations
python manage.py migrate
# Run the server
python manage.py runserver 0.0.0.0:8000
