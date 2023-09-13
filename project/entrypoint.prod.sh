#!/bin/sh
set -e

echo "Development mode"

if [ "$DB_TYPE" = "postgres" ]
then
    echo "Waiting for PostgreSQL to start..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL succesfully started!."
fi

exec "$@"