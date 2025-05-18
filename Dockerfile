FROM python:3.10-slim

WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/base.txt requirements/development.txt requirements/production.txt* /code/requirements/
RUN pip install --no-cache-dir -r /code/requirements/production.txt

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD gunicorn wanderlustai_backend.wsgi:application --bind 0.0.0.0:$PORT 