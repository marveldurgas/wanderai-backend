#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements/base.txt
pip install -r requirements/development.txt
pip install -r requirements/production.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py makemigrations
python manage.py migrate