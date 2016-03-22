from django.core.cache.backends.locmem import LocMemCache
from base_classes import CacheBase
from hydro.common.configurator import Configurator

__author__ = 'moshebasanchig'


class InMemoryCache(CacheBase):

    def __init__(self, params=None):
        self.cache = LocMemCache(name='Hydro', params={})

    def get(self, key):
        try:
            value = self.cache.get(key)
        except Exception, err:
            value = None
        return value

    def put(self, key, value, ttl=Configurator.CACHE_IN_MEMORY_KEY_EXPIRE):
        # just in case the default was changed during the running
        if ttl > Configurator.CACHE_IN_MEMORY_KEY_EXPIRE:
            ttl = Configurator.CACHE_IN_MEMORY_KEY_EXPIRE

        self.cache.set(key, value, ttl)

if __name__ == '__main__':

    from time import sleep
    key = 'a'
    val = {1: 1}

    cache = InMemoryCache()
    cache.put(key, val, None)
    sleep(5)
    print cache.get(key)