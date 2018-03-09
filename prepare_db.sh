#!/bin/bash -x
# This scripts waits for postgres to be ready to accept connections for 20 seconds
# If we run out of time, an exit status of 1 is returned.

DBNAME=${DBNAME:-flat_box}
DATABASE_HOST=db
export PGPASSWORD=postgres

echo "Using database ${DBNAME}"
echo "Waiting for postgres to be ready"

set +e
count=0
while true; do
  psql -c '\q' -h db -U postgres 2>/dev/null
  if [ $? -eq 0 ]; then
    break
  fi
  count=$(($count + 1))
  if [ ${count} -gt 20 ]; then
    echo "Postgres seems to be failing to start"
    exit 1
  fi
  echo -n "."
  sleep 1
done
set -e

echo "Postgres is ready"

# echo "[*] Creating database if needed..."
PGPASSWORD=postgres createdb $DBNAME -h db -U postgres -O postgres -w || true

## uncomment if data is needed
psql postgresql://postgres:postgres@db/flat_box -f ./migrations/V1__Apartments_Table.sql

echo "Data is loaded"
