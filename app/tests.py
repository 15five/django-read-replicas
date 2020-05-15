import time

from django.test import SimpleTestCase
from django.conf import settings

from .models import Item


class ReplicaLagTestCase(SimpleTestCase):
    databases = '__all__'

    def test_replica_lag_item_not_immediatley_present(self):
        i = Item.objects.create(
            name='Thing',
        )

        result = Item.objects.using(settings.DB_ALIAS_MASTER).filter(id=i.id).first()
        self.assertIsNotNone(result)

        result = Item.objects.using(settings.DB_ALIAS_REPLICA_1).filter(id=i.id).first()
        self.assertIsNone(result)

        time.sleep(2)

        result = Item.objects.using(settings.DB_ALIAS_REPLICA_1).filter(id=i.id).first()
        self.assertIsNotNone(result)
