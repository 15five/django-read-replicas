#!/bin/bash

if [ -z "$MASTER_HOST" ]; then
    MASTER_HOST=master
fi

if [ -z "$MASTER_PORT" ]; then
    MASTER_PORT=5432
fi

if [ -z "$REPLICATION_USER" ]; then
    REPLICATION_USER=repuser
fi

if [ -z "$REPLICATION_PASS" ]; then
    REPLICATION_PASS=pass
fi

echo "Setting replication credentials"
echo "*:*:*:$REPLICATION_USER:$REPLICATION_PASS" >> ~/.pgpass
chmod 600 ~/.pgpass

echo "Running pg_basebackup as $REPLICATION_USER"
until pg_basebackup -h $MASTER_HOST -p $MASTER_PORT -D "$PGDATA" -U $REPLICATION_USER --verbose
do
    echo "Waiting for master to open port..."
    sleep 1
done

echo "Configuring postgreql.conf"
echo "listen_addresses = '*'" >> "$PGDATA/postgresql.conf"
echo "hot_standby = on" >> "$PGDATA/postgresql.conf"
sed -i 's/wal_level = hot_standby/wal_level = replica/g' "${PGDATA}/postgresql.conf"

echo "Writing recovery.conf file"
bash -c "cat > $PGDATA/recovery.conf <<- _EOF1_
  standby_mode = 'on'
  primary_conninfo = 'host=$MASTER_HOST port=$MASTER_PORT user=$REPLICATION_USER password=$REPLICATION_PASS'
  trigger_file = '/tmp/postgresql.trigger'
_EOF1_
"

echo "Setting permissions for new data directory"
chown -R postgres:postgres "$PGDATA"
chmod -R 0700 "$PGDATA"

echo "Handing off to CMD args"
exec "$@"

