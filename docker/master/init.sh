if [ -z "$REPLICATION_USER" ]; then
    REPLICATION_USER=repuser
fi

if [ -z "$REPLICATION_PASS" ]; then
    REPLICATION_PASS=pass
fi

echo "Create replication directory"
mkdir "$PGDATA/archivedir"

echo "Add replication configuration"
echo "host replication $REPLICATION_USER 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

cat >> "$PGDATA/postgresql.conf" <<EOF

wal_level = hot_standby
hot_standby = on
archive_mode = on
archive_command = 'cd .'
max_wal_senders = 8
wal_keep_segments = 8

EOF

echo "Create replication role"
psql --username "$POSTGRES_USER" \
     --dbname "$POSTGRES_DB" <<-EOSQL
CREATE ROLE $REPLICATION_USER
  WITH CREATEDB
       LOGIN
       REPLICATION
       CONNECTION LIMIT 100
       ENCRYPTED PASSWORD '$REPLICATION_PASS';
EOSQL

