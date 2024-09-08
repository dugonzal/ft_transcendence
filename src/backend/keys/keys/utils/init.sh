#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

mkdir -p /keys/secrets

openssl genrsa -out /keys/secrets/private.pem 2048

sleep 1
openssl rsa -in /keys/secrets/private.pem -pubout -out /keys/secrets/public.pem

echo "Applying database migrations..."
python manage.py migrate --noinput

# Start the Django development server
echo "Starting Django development server..."
gunicorn --bind 0.0.0.0:80 config.wsgi:application --reload --timeout 120
