FROM postgis/postgis:10-2.5

# If True only minimal database for running tests will be setup.
# If False additional data for development will be downloaded.
ARG OQT_TEST_DB

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

# Download development data if ENV OQT_TEST_DB is False
# This can not be done during init db by Postgres (Permission error)
COPY schema.dev.sh .
# Download schema.dev.sql
RUN bash schema.dev.sh
# Do not fail if schema.dev.sql does not exist
RUN mv schema.dev.sql /docker-entrypoint-initdb.d/3-schema.dev.sql || true

# Initialization scripts.
COPY init-db.sql /docker-entrypoint-initdb.d/1-init-db.sql
COPY schema.test.sql /docker-entrypoint-initdb.d/2-schema.test.sql
COPY post-init-db.sql /docker-entrypoint-initdb.d/4-post-init-db.sql
