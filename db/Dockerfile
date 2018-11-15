FROM mdillon/postgis:11-alpine

# Default password for 'hstorms' user
ENV HSTORMS_PASS=hstorms

COPY init/hstorms_initdb.sh /docker-entrypoint-initdb.d
# TODO solve dump location
COPY data/hstorms_dump.gz /docker-entrypoint-initdb.d
