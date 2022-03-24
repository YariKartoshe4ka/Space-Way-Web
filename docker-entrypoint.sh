#!/bin/bash

# Wait for database to start
sleep 10

# Configure database
python manage.py makemigrations
python manage.py migrate

# Create SuperUser
python manage.py createsuperuser --no-input

# Start server
python manage.py runserver 0.0.0.0:8000
