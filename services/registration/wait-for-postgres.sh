#!/bin/bash
# Waits for Postgres startup then executes the command.
set -e

db_url_regex="^[a-zA-Z]+://([a-zA-Z0-9]+):([a-zA-Z0-9]+)@([-_.a-zA-Z0-9]+):[0-9]+/([_a-zA-Z0-9]+)$"

# Regex group name -> index maps.
USER=1
PASSWORD=2
HOST=3
DB=4

if [[ ! $DATABASE_URL =~ $db_url_regex ]]; then
    echo "$DATABASE_URL does not match regex $db_url_regex"
    exit 1
fi

until PGPASSWORD=${BASH_REMATCH[$PASSWORD]} \
            psql --host=${BASH_REMATCH[$HOST]} \
                 --username=${BASH_REMATCH[$USER]} \
                 --dbname=${BASH_REMATCH[$DB]} \
                 -c '\q'; do
    >&2 echo "Tried to connect to ${BASH_REMATCH[$HOST]} as ${BASH_REMATCH[$USER]}"
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $@
