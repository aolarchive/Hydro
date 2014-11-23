__author__ = 'yanivshalev'

from hydro.conf.settings import *
ALL = 'ALL'


class Configuration(object):
    _conf = {}

    def set(self, key, val):
        self._conf[key] = val

    def get(self, key):
        return self._conf[key]

    @property
    def conf(self):
        return self._conf


class Configurator(object):

    """
    api for returning configuration by environment
    """
    APPLICATION_NAME = APPLICATION_NAME
    SECRET_KEY = SECRET_KEY
    TIME_ZONE = TIME_ZONE
    LANGUAGE_CODE = LANGUAGE_CODE
    SECOND = SECOND
    MINUTE = MINUTE
    LOG_DIR = LOG_DIR
    DATABASES = DATABASES
    SECONDS_IN_DAY = SECONDS_IN_DAY
    MYSQL_CACHE_DB = MYSQL_CACHE_DB
    MYSQL_CACHE_TABLE = MYSQL_CACHE_TABLE
    CACHE_IN_MEMORY_KEY_EXPIRE = CACHE_IN_MEMORY_KEY_EXPIRE
    CACHE_DB_KEY_EXPIRE = CACHE_DB_KEY_EXPIRE
    USE_STATS_DB = USE_STATS_DB

    #DB TYPES
    VERTICA = 'VERTICA'
    MYSQL = 'MYSQL'
    HBASE = 'HBASE'
    COUCHBASE = 'COUCHBASE'
    MEMCACHE = 'MEMCACHE'

    #CACHE
    CACHE_ENGINE_MYSQL_CACHE = 'mysql'
    CACHE_ENGINE_IN_MEMORY = 'default'

    OPTIMIZER_STATISTICS = {ALL: {'AVG_VALUES_PER_DAY': None,
                                  'AVG_RECORDS_PER_DAY': None,
                                  'MEDIAN_VALUES_PER_DAY': None,
                                  'MEDIAN_RECORDS_PER_DAY': None,
                                  'AVG_STDDEV': None,
                                  'MEDIAN_STDDEV': None,
                                  'VALUES_LAST_7_DAYS': None,
                                  'VALUES_LAST_14_DAYS': None,
                                  'VALUES_LAST_21_DAYS': None,
                                  'VALUES_LAST_28_DAYS': None,
                                  'VALUES_LAST_60_DAYS': None,
                                  'VALUES_LAST_90_DAYS': None,
                                  'RECORDS_LAST_7_DAYS': None,
                                  'RECORDS_LAST_14_DAYS': None,
                                  'RECORDS_LAST_21_DAYS': None,
                                  'RECORDS_LAST_28_DAYS': None,
                                  'RECORDS_LAST_60_DAYS': None,
                                  'RECORDS_LAST_90_DAYS': None,
                                  },
                            }





    @classmethod
    def config_builder(cls):
        conf = Configuration()
        conf.CONNECTIONS = {}
        return conf

if __name__ == '__main__':
    print Configurator.APPLICATION_NAME
