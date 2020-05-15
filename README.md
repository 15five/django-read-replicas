# Django Read Replicas

This project aims to mimic the delay of replication between master and
replica databases in cloud infrastructure (or elsewhere).

The repo has a few parts:

- docker-compose.yaml: Creates the Postgres Master and Read Replica
- Replica utils/ directory: A directory that holds the logic required to allow Django to utilize the replica in tests
- Django Project: Demo of a project configured to use the utils mentioned above
- Django application: An application with tests that fail if there is too long of a replica lag

To get things running, follow these steps:

1. `$ docker-compose up -d`
2. `$ docker exec -it django-read-replicas_master_1 /delay.sh`
3. `$ python manage.py test`

If you need to specify varying levels of delay, pass a number of 
milliseconds of delay to the delay.sh script in the master container.
3000 is the default.

    docker exec -it django-read-replicas_master_1 /delay.sh 5000

### Troubleshooting

If you need to test that replication lag is in fact present,
try the time-test.sh script in the root of this repo.
