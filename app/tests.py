import time

from django.conf import settings

from replicas.test import ReplicaLagTestCase

from .models import Item


class ItemTestCase(ReplicaLagTestCase):
    def setUp(self):
        self.db_wait(Item)

    def test_replica_lag_item_not_immediatley_present(self):
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
