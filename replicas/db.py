import logging
import threading

from django.conf import settings

logger = logging.getLogger(__name__)

THREAD_LOCAL = threading.local()


class ForceDBReadsFromMaster:
    """
    A singleton to keep track of whether reads should be made from the
    master or replica database.

    We use a "depth" key in this singleton so that calls to "force reads
    from master" from within deeper code do not effect prior calls to
    "force reads from master" made by shallower code.

    func1 call
       start "force reads from master"
       ... do stuff ...
       func2 call
         start "force reads from master"
         ... do stuff ...
         stop "force reads from master" <--
                    we don't want this call to effect the call made by func1

       stop "force reads from master"
    """
    cache_key = 'force_master_db_for_reads_depth'

    @classmethod
    def get_depth(cls):
        return getattr(THREAD_LOCAL, cls.cache_key, None) or 0

    @classmethod
    def set_depth(cls, value):
        logger.debug(f'Setting ForceDBReadsFromMaster depth to {value}')
        setattr(THREAD_LOCAL, cls.cache_key, value)

    @classmethod
    def enter(cls):
        cls.set_depth(cls.get_depth() + 1)

    @classmethod
    def exit(cls):
        cls.set_depth(max(cls.get_depth() - 1, 0))

    def __enter__(self):
        self.enter()

    def __exit__(self, *args):
        self.exit()

    @classmethod
    def active(cls):
        return bool(cls.get_depth())


class MasterReplicaRouter:

    def db_for_read(self, model, **hints):
        return settings.DB_ALIAS_REPLICA_1

    def db_for_write(self, model, **hints):
        # all writes should be sent to master db
        return settings.DB_ALIAS_MASTER

    def allow_relation(self, obj1, obj2, **hints):
        # allow all relations between objects
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # only allow migrations on master db
        return db == settings.DB_ALIAS_MASTER
