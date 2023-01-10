FROM ghcr.io/stac-utils/pgstac:v0.6.11
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=postgis
ENV PGUSER=username
ENV PGPASSWORD=password
ENV PGHOST=localhost
ENV PGDATABASE=postgis
COPY data /data
COPY ingest.sh /docker-entrypoint-initdb.d/z_ingest.sh
