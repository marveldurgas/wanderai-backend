#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if not exists
echo "Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

# Start gunicorn server
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:$PORT wanderlustai_backend.wsgi:application 