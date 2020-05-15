import time

from django.test import SimpleTestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.runner import DiscoverRunner

from . import patches
from . import db


class DiscoverRunnerWithReadReplicas(DiscoverRunner):
    def setup_databases(self, *args, **kwargs):
        # Let's force reads from master while setting up the databases
        # so that we don't have to re-write migrations.
        with db.ForceDBReadsFromMaster():
            return super().setup_databases(*args, **kwargs)

    def teardown_databases(self, old_config, **kwargs):
        from django.db import connections
        for alias in connections:
            if connections[alias].settings_dict['TEST'].get('REPLICA'):
                connections[alias].close()
        super().teardown_databases(old_config, **kwargs)


class ReplicaLagTestCase(SimpleTestCase):
    databases = '__all__'

    def db_wait(self, model=get_user_model()):
        print('Waiting for master ', end='', flush=True)
        while True:
            try:
                model.objects.using(settings.DB_ALIAS_MASTER).filter(id=0).first()
                print('done', flush=True)
                break
            except Exception:
                time.sleep(1)
                print('.', end='', flush=True)

        print('Waiting for replica ', end='', flush=True)
        while True:
            try:
                model.objects.using(settings.DB_ALIAS_REPLICA_1).filter(id=0).first()
                print('done', flush=True)
                break
            except Exception:
                time.sleep(1)
                print('.', end='', flush=True)

    def setUp(self):
        super().setUp()

        self.db_wait()
