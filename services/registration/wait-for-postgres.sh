#!/bin/bash
# Waits for Postgres startup then executes the command.
set -e

DATABASE_URL=postgres://cbbyslspigkjpj:6bdfce2156b7a67dc4fb1f25473158ef38fb8b29621e6f9965abdb94d75e9852@ec2-54-83-29-34.compute-1.amazonaws.com:5432/dab7ehmia5n9vf
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
