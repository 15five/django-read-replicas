import time

from django.test import SimpleTestCase
from django.conf import settings

from .models import Item


class ReplicaLagTestCase(SimpleTestCase):
    databases = '__all__'

    def db_wait(self):
        print('Waiting for master', end='', flush=True)
        while True:
            try:
                Item.objects.using(settings.DB_ALIAS_MASTER).filter(id=0).first()
                print(' done', flush=True)
                break
            except Exception:
                time.sleep(1)
                print('.', end='', flush=True)

        print('Waiting for replica', end='', flush=True)
        while True:
            try:
                Item.objects.using(settings.DB_ALIAS_REPLICA_1).filter(id=0).first()
                print(' done', flush=True)
                break
            except Exception:
                time.sleep(1)
                print('.', end='', flush=True)

    def test_replica_lag_item_not_immediatley_present(self):
        self.db_wait()

        i = Item.objects.create(
            name='Thing',
        )

        result = Item.objects.using(settings.DB_ALIAS_MASTER).filter(id=i.id).first()
        self.assertIsNotNone(result)

        result = Item.objects.using(settings.DB_ALIAS_REPLICA_1).filter(id=i.id).first()
        self.assertIsNone(result)

        time.sleep(4)

        result = Item.objects.using(settings.DB_ALIAS_REPLICA_1).filter(id=i.id).first()
        self.assertIsNotNone(result)
