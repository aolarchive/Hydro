from hydro.common.configurator import Configurator
from base_classes import CacheBase
from hydro.cache.in_memory import InMemoryCache
from django.core.management.commands import createcachetable
from pandas.core.frame import DataFrame
from django.db.utils import DatabaseError
from django.core.cache.backends.db import DatabaseCache

__author__ = 'moshebasanchig'


class MySQLCache(CacheBase):
    def __init__(self, params=None):
        self.in_mem = InMemoryCache()

        if params is None:
            params = dict()
        cache_table = params.get('cache_table', Configurator.MYSQL_CACHE_TABLE)
        cache_db = params.get('cache_db', Configurator.MYSQL_CACHE_DB)

        self.cache = DatabaseCache(cache_table, params={'NAME': cache_db})

        # creating a table if not exist
        try:
            self.cache.get('a')
        except Exception, err:
            if err.args[0] in (1146, 1049):  # 1146 - table doesn't exist, 1049 - unknown database?
                cmd = createcachetable.Command().execute(cache_table,
                                                         **{'database': cache_db,
                                                            'verbosity': 2})
            else:
                raise

    def get(self, key):
        empty = lambda value: isinstance(value, DataFrame) or (not isinstance(value, DataFrame) and value)
        value = self.in_mem.get(key)
        if not empty(value):
            value = self.cache.get(key)
            # assuming that in case of db key expired, the worse case will be the additional of in memory expiration
            # time
            if not empty(value):
                self.in_mem.put(key, value)
        return value

    def put(self, key, value, ttl=Configurator.CACHE_DB_KEY_EXPIRE):
        #just in case the default was changed during the running
        if ttl > Configurator.CACHE_DB_KEY_EXPIRE:
            ttl = Configurator.CACHE_DB_KEY_EXPIRE
        try:
            self.cache.set(key, value, ttl)
        except DatabaseError as ex:
            # e.g the stored value exceeds the max_packet_size (that should raise DatabaseError or OperationalError)
            self.logger.error('Failed adding an item to the cache: ' + ex)
            pass
        self.in_mem.put(key, value, min(Configurator.CACHE_IN_MEMORY_KEY_EXPIRE, ttl))

if __name__ == '__main__':

    key = 'ddabbb'
    val = {1: 1}

    class JJ():
        x = 'a'

    val = JJ()
    cache = MySQLCache()
    #cache.put(key=key, value=val, ttl=None)
    print  cache.get(key=key)