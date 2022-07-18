FROM postgis/postgis:10-2.5

RUN  apt-get update \
  && apt-get install -y wget gzip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /docker-entrypoint-initdb.d

# Copy script for index creation
COPY create-index.sql .

# Get postgres dump
RUN wget https://downloads.ohsome.org/OQT/dump.sql.gz
RUN gzip -d dump.sql.gz

# Set initialization order
RUN mv dump.sql 1-dump.sql
RUN mv create-index.sql 2-create-index.sql
