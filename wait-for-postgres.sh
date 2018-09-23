#!/bin/bash
# Waits for Postgres startup then executes the command.
set -e

cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "postgres" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
