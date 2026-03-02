FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files (use placeholder secret key for build)
RUN SECRET_KEY=build-placeholder \
    DJANGO_SETTINGS_MODULE=gestione_comune.settings.production \
    python manage.py collectstatic --noinput

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN mkdir -p /app/media /app/logs && chown -R appuser:appgroup /app/media /app/logs
USER appuser

EXPOSE 8000

# Default CMD - shell form to expand $PORT (Render sets PORT env var)
CMD /app/entrypoint.sh gunicorn gestione_comune.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
