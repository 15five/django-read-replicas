FROM postgres:11-alpine

# Installed for "tc" command used in delay.sh
RUN apk add iproute2

COPY init.sh /docker-entrypoint-initdb.d/init.sh

