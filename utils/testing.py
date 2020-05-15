from django.test.runner import DiscoverRunner

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


def patch_db_wrapper():
    from django.db import DEFAULT_DB_ALIAS, connections
    from django.db.backends.postgresql import base
    from django.db.backends.base.creation import TEST_DATABASE_PREFIX

    class DatabaseWrapper(base.DatabaseWrapper):
        def get_connection_params(self):
            settings_dict = self.settings_dict
            test_db_name = TEST_DATABASE_PREFIX + self.settings_dict['NAME']
            is_same_db = connections[DEFAULT_DB_ALIAS].settings_dict['NAME'] == test_db_name
            if self.settings_dict['TEST'].get('REPLICA') and is_same_db:
                settings_dict['NAME'] = test_db_name

            return super().get_connection_params()

    base.DatabaseWrapper = DatabaseWrapper


patch_db_wrapper()


def patch_get_unique_databases_and_mirrors():
    import collections

    from django.db import DEFAULT_DB_ALIAS, connections
    # need to create patch get_unique_databases_and_mirrors in utils
    from django.test import utils

    def get_unique_databases_and_mirrors(aliases=None):
        """
        Figure out which databases actually need to be created.

        De-duplicate entries in DATABASES that correspond the same database or are
        configured as replicas.

        Return two values:
        - test_databases: ordered mapping of signatures to (name, list of aliases)
                          where all aliases share the same underlying database.
        - mirrored_aliases: mapping of mirror aliases to original aliases.
        """
        if aliases is None:
            aliases = connections
        mirrored_aliases = {}
        test_databases = {}
        dependencies = {}
        default_sig = connections[DEFAULT_DB_ALIAS].creation.test_db_signature()

        for alias in connections:
            connection = connections[alias]

            test_settings = connection.settings_dict['TEST']

            if test_settings.get('REPLICA'):
                # If the connection is marked as a replica, assume that the
                # mirroring logic will be handled at the database layer.
                pass
            elif test_settings['MIRROR']:
                # If the database is marked as a test mirror, save the alias.
                mirrored_aliases[alias] = test_settings['MIRROR']
            elif alias in aliases:
                # Store a tuple with DB parameters that uniquely identify it.
                # If we have two aliases with the same values for that tuple,
                # we only need to create the test database once.
                item = test_databases.setdefault(
                    connection.creation.test_db_signature(),
                    (connection.settings_dict['NAME'], set())
                )
                item[1].add(alias)

                if 'DEPENDENCIES' in test_settings:
                    dependencies[alias] = test_settings['DEPENDENCIES']
                else:
                    if alias != DEFAULT_DB_ALIAS and connection.creation.test_db_signature() != default_sig:
                        dependencies[alias] = test_settings.get('DEPENDENCIES', [DEFAULT_DB_ALIAS])

        test_databases = utils.dependency_ordered(test_databases.items(), dependencies)
        test_databases = collections.OrderedDict(test_databases)
        return test_databases, mirrored_aliases

    utils.get_unique_databases_and_mirrors = get_unique_databases_and_mirrors


patch_get_unique_databases_and_mirrors()
