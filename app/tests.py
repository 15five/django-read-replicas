import time

from django.test import TestCase
from django.conf import settings

from .models import Item


class ReplicaLagTestCase(TestCase):
    def test_replica_lag_item_not_immediatley_present(self):
        i = Item.objects.create(
            name='Thing',
        )

        result = Item.objects.using(settings.DB_ALIAS_MIRROR_1).filter(id=i.id).first()
        self.assertIsNone(result)

        time.sleep(2)

        result = Item.objects.using(settings.DB_ALIAS_MIRROR_1).filter(id=i.id).first()
        self.assertIsNotNone(result)
