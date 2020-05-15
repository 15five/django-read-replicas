# Django Read Replicas

This project aims to mimic the delay of replication between master and
replica databases in cloud infrastructure (or elsewhere).

The repo has a few parts:

- docker-compose.yaml: Creates the Postgres Master and Read Replica
- Replica replicas/ directory: A directory that holds the logic required to allow Django to utilize the replica in tests
- Django Project: Demo of a project configured to use the replica mentioned above
- Django application: An application with tests that test for an expected level of delay

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

### TODO

1. Explain project settings:

    DATABASES[DB_ALIAS_MASTER]['AUTOCOMMIT'] = True

    DB_ALIAS_REPLICA_1 = 'replica1'
    DATABASES[DB_ALIAS_REPLICA_1] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PGDATABASE') or 'drr',
        'USER': os.environ.get('PGUSER') or 'drr_user',
        'PASSWORD': os.environ.get('PGPASSWORD') or 'pass',
        'HOST': os.environ.get('PGHOST_REPLICA_1') or 'localhost',
        'PORT': int(os.environ.get('PGPORT_REPLICA_1') or 5433),
        'TEST': {
            # Non-standard Django DATABASES > TEST key for use in DRR
            'REPLICA': True,
        }
    }

    DATABASE_ROUTERS = ['replicas.db.MasterReplicaRouter']

    TEST_RUNNER = 'replicas.test.DiscoverRunnerWithReadReplicas'

2. Explain how to setup a test like the one in app/tests.py. Ie. Explain what the db_wait method does and why.
3. Package project for installation from PyPI.
4. Write article about this tool and why it was created

