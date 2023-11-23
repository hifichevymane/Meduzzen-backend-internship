#!/bin/sh
# Creating migrations if they are
python manage.py makemigrations
# Apply migrations
python manage.py migrate
# Collect static files for production
python manage.py collectstatic --no-input
# Run the server
python manage.py runserver 0.0.0.0:8000
