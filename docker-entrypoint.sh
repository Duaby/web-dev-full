#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Django application..."

# Wait for database to be ready (if using PostgreSQL)
if [ "$DATABASE_ENGINE" = "postgresql" ]; then
    echo "⏳ Waiting for PostgreSQL to be ready..."
    
    while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; do
        echo "⏳ PostgreSQL is unavailable - sleeping..."
        sleep 2
    done
    
    echo "✅ PostgreSQL is ready!"
fi

# Apply database migrations
echo "📦 Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create cache table (if using database cache)
# python manage.py createcachetable

echo "✅ Setup complete!"

# Execute the main command (passed as arguments to this script)
exec "$@"