#!/bin/bash
set -e

echo "Waiting for database..."
while ! python -c "
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestione_comune.settings.production')
import django; django.setup()
from django.db import connections
try:
    connections['default'].cursor()
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    echo "Database not ready, waiting..."
    sleep 2
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if env vars are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput 2>/dev/null || true
    echo "Superuser check complete."
fi

echo "Starting server..."
exec "$@"
