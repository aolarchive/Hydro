from hydro.common.configurator import Configurator

__author__ = 'moshebasanchig'


class CacheEnginesFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def get_cache_engines():
        from .in_memory import InMemoryCache
        from .mysql_cache import MySQLCache

        return {Configurator.CACHE_ENGINE_IN_MEMORY: InMemoryCache,
                Configurator.CACHE_ENGINE_MYSQL_CACHE: MySQLCache}
