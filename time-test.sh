export PGPASSWORD=pass
psql -h localhost -p 5432 -U drr_user -d drr -c "DROP TABLE IF EXISTS time_test;"
psql -h localhost -p 5432 -U drr_user -d drr -c "CREATE TABLE time_test (t TIMESTAMP);"

echo "Beginning time test. Please use the following command to watch the replciation..."
echo
echo "while true; do PGPASSWORD=pass psql -h localhost -p 5433 -U drr_user -d drr -c 'SELECT * FROM time_test ORDER BY t DESC LIMIT 1;'; sleep 1; done"
echo

while true;
do
    echo Inserting $(date)
    psql -h localhost -p 5432 -U drr_user -d drr -c "INSERT INTO time_test VALUES (now());"
    sleep 1;
done
