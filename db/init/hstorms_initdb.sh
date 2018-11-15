#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER hstorms WITH ENCRYPTED PASSWORD '$HSTORMS_PASS';
    CREATE DATABASE hstorms;
    GRANT ALL PRIVILEGES ON DATABASE hstorms TO hstorms;
EOSQL

gunzip -c /docker-entrypoint-initdb.d/hstorms_dump.gz | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" hstorms
