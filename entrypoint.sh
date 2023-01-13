#!/bin/sh
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres database ..."
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
    done
    echo "Database PostgreSQL started"
fi

echo "Preparing migrations and  updating the database. "
python manage.py makemigrations main --noinput
python manage.py migrate --noinput
exec "$@"

# Start server
echo "Starting server"
python manage.py runserver localhost:8000