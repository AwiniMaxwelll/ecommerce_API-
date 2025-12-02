#!/bin/bash
set -e  # Exit on any error

echo "🚀 Starting E-Commerce API Deployment..."

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic --noinput

# Create superuser if needed (optional, for dev)
# python manage.py createsuperuser --noinput || true

# Start the server with Gunicorn (4 workers, bind to Railway's PORT)
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 ecommerce_backend.wsgi:application