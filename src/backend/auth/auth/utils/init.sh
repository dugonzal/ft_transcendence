#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

# Fetch public key from JWT Key Management Service
if [ ! -f /auth/secrets/jwt_auth_public.pem ]; then
  mkdir -p auth/secrets
  curl -o /usr/src/app/secrets/jwt_auth_public.pem http://keys:8000/api/key/public-key/
  # Validate the fetched key (optional check)
  if ! openssl rsa -pubin -in /auth/secrets/jwt_auth_public.pem -text -noout >/dev/null 2>&1; then
    echo "Error: Fetched public key is not valid."
    exit 1
  fi
fi

# Fetch private key from JWT Key Management Service
if [ ! -f /auth/secrets/jwt_auth_private.pem ]; then
  curl -o /usr/src/app/secrets/jwt_auth_private.pem http://keys:8000/api/key/private-key/
  # Validate the fetched key (optional check)
  if ! openssl rsa -in /auth/secrets/jwt_auth_private.pem -check >/dev/null 2>&1; then
    echo "Error: Fetched private key is not valid."
    exit 1
  fi
fi

# Apply database migrations first time
echo "Applying database migrations..."
if ! python manage.py makemigrations authentication --noinput; then
  echo "Migrations failed"
  exit 1
fi

# Apply database migrations
#echo "Applying database migrations..."
#if ! python manage.py migrate --noinput; then
#  echo "Migrations failed"
#  exit 1
#fi

# Collect static files
echo "Collecting static files..."
if ! python manage.py collectstatic --no-input; then
  echo "Collectstatic failed"
  exit 1
fi

# Start the Django development server
echo "Starting Django development server..."
gunicorn --bind 0.0.0.0:80 --workers=3 config.wsgi:application --reload --timeout 120
