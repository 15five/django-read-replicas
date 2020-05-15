# Django Read Replicas

This project aims to mimic the delay of replication between master and
replica databases in cloud infrastructure (or elsewhere).

The repo has a few parts:

- docker-compose.yaml: Creates the Postgres Master and Read Replica
- replica utils: A directory that holds the logic required to allow Django to utilize the replica in tests
- Django Project: Demo of a project configured to use the utils mentioned above
- Django application: An application with tests that fail if there is too long of a replica lag


The project defines some environment variables that are used to connect to the databases.
If these are not defined in the runtime environment of the project, defaults are used. Please note,
that the docker containers will also need to be rebuilt if the username/password credentials change.

PGDATABASE

PGUSER
PGPASSWORD

PGHOST
PGPORT

PGHOST_REPLICA_1
PGPORT_REPLICA_1




TODO:



Update https://github.com/15five/postgres.master - delay.sh

