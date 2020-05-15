FROM postgres:11-alpine

# Installed for "tc" command used in delay.sh
RUN apk add iproute2

COPY init.sh /docker-entrypoint-initdb.d/init.sh
COPY delay.sh /delay.sh
RUN chmod 0777 delay.sh
