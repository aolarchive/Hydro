__author__ = 'moshebasanchig'

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydro.conf.settings'
from django.core.cache import get_cache
from base_classes import CacheBase
from hydro.common.configurator import Configurator


class InMemoryCache(CacheBase):

    def __init__(self, params=None):
        self.cache = get_cache('django.core.cache.backends.locmem.LocMemCache')

    def get(self, key):
        try:
            value = self.cache.get(key)
        except Exception, err:
            value = None
        return value

    def put(self, key, value, ttl=Configurator.CACHE_IN_MEMORY_KEY_EXPIRE):
        #just in case the default was changed during the running
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