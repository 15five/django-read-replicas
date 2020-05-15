FROM postgres:11-alpine

RUN apk add --update iputils

COPY docker-entrypoint.custom.sh /docker-entrypoint.sh

RUN chmod 0755 /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

USER postgres

CMD postgres -D $PGDATA

